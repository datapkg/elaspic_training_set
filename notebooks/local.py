import logging
import datetime

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


def get_templates(x):

    unique_id, uniprot_id, uniprot_mutation, domain_def, uniprot_sequence = x

    try:
        result_df, system_command = run_blast(uniprot_id, uniprot_sequence, domain_def)
        if result_df is None or len(result_df) == 0:
            raise Exception('No templates were found in the PDB database!')
        result_df['unique_id'] = unique_id

        blast_results_mutdom = remove_domains_outside_mutation(result_df, uniprot_mutation)
        if blast_results_mutdom is None or len(blast_results_mutdom) == 0:
            raise Exception('Templates that were found do not cover the site of the mutation!')

    except Exception as e:
        print(
            'An error occured!\n',
            e, '\n',
            uniprot_id, ' ', domain_def, ' ', uniprot_mutation, '\n',
            # uniprot_sequence, '\n',
            sep='',
        )
        return None

    return blast_results_mutdom


def remove_domains_outside_mutation(result_df, mutation):
    result_df = (
        result_df[
            result_df['domain_def_new']
            .apply(lambda x: mutation_inside_domain([mutation, x]))
        ].copy()
    )
    return result_df


def get_max_seq_identity(alignment_identity):
    """
    Examples
    --------
    >>> get_max_seq_identity(90.63)
    100
    >>> get_max_seq_identity(81.54)
    100
    >>> get_max_seq_identity(71.2)
    80
    >>> get_max_seq_identity(59.3)
    60
    >>> get_max_seq_identity(11.1)
    40
    """
    assert (alignment_identity <= 100) & (alignment_identity > 1.0)
    if alignment_identity > 80:
        return 100
    elif alignment_identity > 60:
        return 80
    elif alignment_identity > 40:
        return 60
    return 40
