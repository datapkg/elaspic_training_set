import logging
import datetime
import pandas as pd

logger = logging.getLogger(__name__)


def annotate_blast_results(result_df, domain_start, domain_sequence_length):
    """Add additional information to blast results.

    .. note::

        This code is used for parsing Profs libraries, and may have to be adapted
        for for libraries following a different format.
    """
    result_df = result_df.copy()

    if result_df.empty:
        return result_df

    if result_df['subject_id'].values[0].count('|') == 2:
        HEADER_TYPE = 1
    elif result_df['subject_id'].values[0].count('|') == 5:
        HEADER_TYPE = 2
    else:
        raise Exception

    # Parse blast results
    result_df['pdb_id'] = result_df['subject_id'].apply(lambda x: x.split('|')[0].split('_')[0])
    result_df['pdb_chain'] = result_df['subject_id'].apply(lambda x: x.split('|')[0].split('_')[1])
    result_df['pdb_pdbfam_name'] = result_df['subject_id'].apply(lambda x: x.split('|')[1])
    result_df['pdb_pdbfam_idx'] = result_df['subject_id'].apply(lambda x: int(x.split('|')[2]))
    if HEADER_TYPE == 2:
        result_df['pdb_pfam_clan'] = result_df['subject_id'].apply(lambda x: x.split('|')[3])
        result_df['pdb_domain_def'] = result_df['subject_id'].apply(lambda x: x.split('|')[4])
        result_df['pdb_cath_id'] = result_df['subject_id'].apply(lambda x: x.split('|')[5])

    # Score sequence identity
    alpha = 0.95
    result_df['alignment_identity'] = result_df['pc_identity']
    result_df['alignment_coverage'] = (
        (result_df['q_end'] - result_df['q_start'] + 1) / float(domain_sequence_length) * 100.0
    )
    result_df['alignment_score'] = (
        alpha * (result_df['alignment_identity'].values / 100) *
        (result_df['alignment_coverage'].values / 100) +
        (1 - alpha) * (result_df['alignment_coverage'].values / 100)
    )

    # Domain definitions
    result_df['domain_start_new'] = domain_start + result_df['q_start'].astype(int) - 1
    result_df['domain_end_new'] = domain_start + result_df['q_end'].astype(int) - 1
    result_df['domain_def_new'] = (
        result_df['domain_start_new'].astype(str) + ':' +
        result_df['domain_end_new'].astype(str)
    )
    result_df['t_date_modified'] = datetime.datetime.now()
    return result_df


def get_max_seq_identity(alignment_identity):
    """
    Examples
    --------
    >>> get_max_seq_identity(0.9063)
    100
    >>> get_max_seq_identity(0.8154)
    100
    >>> get_max_seq_identity(0.712)
    80
    >>> get_max_seq_identity(0.593)
    60
    >>> get_max_seq_identity(0.111)
    40
    """
    assert (alignment_identity <= 1) & (alignment_identity > 0.1)
    if alignment_identity > 0.8:
        return 100
    elif alignment_identity > 0.6:
        return 80
    elif alignment_identity > 0.4:
        return 60
    return 40


# === Standalone pipeline functions ===

def get_partner_chain(protein, pdb_chain):
    """
    Examples
    --------
    >>> get_partner_chain('1CSE_E_I', 'E_A1C')
    'I'
    """
    _, chain1, chain2 = protein.split('_')
    if len(chain1) > len(chain2):
        chain2 = chain2 + chain2[-1] * (len(chain1) - len(chain2))
    if len(chain2) > len(chain1):
        chain1 = chain1 + chain1[-1] * (len(chain2) - len(chain1))
    for a, b in zip(chain1, chain2):
        if a == pdb_chain:
            return b
        if b == pdb_chain:
            return a
    print(protein, pdb_chain, chain1, chain2)
    raise Exception

    
def get_partner_uniprot_id(uniprot_id, uniprot_id_1, uniprot_id_2):
    if uniprot_id == uniprot_id_1:
        return uniprot_id_2
    return uniprot_id_1


# ===

def get_core_mutation_features(index, mutation_json):
    df = pd.DataFrame(mutation_json)
    if 'idxs' in df.columns:
        df = df[df['idxs'].isnull()]
    if df.empty:
        return None
    df.index = [index] * df.shape[0]
    return df


mutation_not_in_interface = 0
mutation_interface_not_found = 0


def guess_interface_mutation_features(index, mutation_json):
    global mutation_not_in_interface
    global mutation_interface_not_found

    df = pd.DataFrame(mutation_json)
    if 'idxs' not in df.columns:
        mutation_not_in_interface += 1
        return None
    df = df[df['idxs'].notnull()]
    df.index = [index] * df.shape[0]
    if df.empty:
        mutation_interface_not_found += 1
    return df


def get_interface_mutation_features(index, idxs, mutation_json):
    global mutation_not_in_interface
    global mutation_interface_not_found

    df = pd.DataFrame(mutation_json)
    if 'idxs' not in df.columns:
        mutation_not_in_interface += 1
        return None
    df = df[df['idxs'].notnull()]
    df = df[df['idxs'].apply(lambda x: (tuple(sorted(x)) == idxs)).astype(bool)]
    df.index = [index] * df.shape[0]
    if df.empty:
        mutation_interface_not_found += 1
    return df
