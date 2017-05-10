def tl_to_matrix(tokenlist_df, tokens, sparse=False):
    ''' Get a vector of token counts for a volume, in the order
    of the `tokens` list.
    
    i.e.
           tokens[0] tokens[1] ... tokens[n]
    volid    count      count  ...  count
    
    Recommended to use with `sparse=True`, which
    uses SciPy's Sparse Matrix format rather than saving zero-counts for
    the entire vocabulary that isn't in the volume.
    
    The tokenlist currently cannot include a pos column and does not support pages (you
    can apply this function page-by-page, though). 
    
    The ideal input, then, is from vol.tokenlist(pages=False, pos=False)
    '''
    # Check if 'lowercase' column exists, rename to 'token'
    colnames = list(tokenlist_df.index.names)
    if 'lowercase' in colnames:
        tokenlist_df = tokenlist_df.copy()
        colnames[colnames.index('lowercase')] = 'token'
        tokenlist_df.index.names = colnames
    
    tl_matrix = pd.merge(tokens, tokenlist_df.reset_index()[['token', 'count']], on="token", how="left")\
                  .fillna(0)['count']\
                  .values.T
            
    if sparse:
        return (vol.id, sparse.csr_matrix(tl_matrix).astype("uint16"))
    else:
        return (vol.id, tl_matrix.astype("uint16"))
    
def csr_matrix_to_gensim(csr_matrix):
    # Gensim wants a representation where each doc is a list of tuples in the form (id, count)
    # The CSR sparse matrix format saves this well: for a 1-d row, data gives you counts and indices gives
    # you the id reference (which should match the token reference)
    rows = all_vol_arrs.shape[0]
    docs = [csr_row_to_gensim(all_vol_arrs.getrow(i)) for i in range(0, rows)]
    return docs

def csr_row_to_gensim(csr_row):
    counts = csr_row.data
    tokenids = csr_row.indices
    a = np.dstack([tokenids, counts])[0]
    gensim_doc = list(map(tuple, a))
    return gensim_doc
