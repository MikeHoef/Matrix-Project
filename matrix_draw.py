
Colors =["\"white\"", "\"black\"","\"red\"", "\"blue\""]

def graphviz_matrix_color(label, rows):

    S = str(label) + ' [label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\"> \n'
    m = len(rows[0])
    for r in rows:
        row ='<TR>'
        for i in range(m-1):
            row = row + '<TD ' + 'BGCOLOR=' + Colors[r[i]] + '>   </TD>'
        row = row + '</TR> \n'
        S = S + row
    S = S + '</TABLE>>]; \n'
    return S



def transitive_reduction(rels):

    Relations = rels[:]

    while True:
        size = len(Relations)
        for a in rels:
            for b in rels:
                if a[1] == b[0]:
                    if (a[0], b[1]) in Relations:
                        Relations.remove((a[0], b[1]))
        if size == len(Relations):
            break

    return Relations



def graphviz_hasse(mats, rels):

    S ='digraph G{\n node [shape=plaintext] \n \n rankdir=\"LR\" \n\n'
    for i in range(len(mats)):
        S = S + graphviz_matrix_color(i, mats[i].rows)

    Relations = transitive_reduction(rels)

    for r in Relations:
        S = S + str(r[0]) + '->' + str(r[1]) + '\n'
    S = S + '\n }'
    return S
