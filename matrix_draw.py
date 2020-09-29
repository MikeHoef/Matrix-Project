
Colors =["\"whitesmoke\"", "\"slategray\"","\"darkslategray\"", "\"grey2\""]
Highlighted_Colors =["\"lightgoldenrodyellow\"", "\"lightgoldenrod4\"","\"lightsalmon4\"", "\"grey2\""]


def graphviz_matrix(label, rows):

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

def graphviz_matrix_highlighted(label, rows):

    S = str(label) + ' [label=<<TABLE BORDER=\"1\" CELLBORDER=\"1\" CELLSPACING=\"0\"> \n'
    m = len(rows[0])
    for r in rows:
        row ='<TR>'
        for i in range(m-1):
            row = row + '<TD ' + 'BGCOLOR=' + Highlighted_Colors[r[i]] + '>   </TD>'
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



def graphviz_hasse(mats, rels, orient='BT', splines='ortho', ranksep=1, nodesep=1,arrowhead='none', highlighted=[]):

    S ='digraph G{\n node [shape=plaintext] \n \n rankdir=\"' + str(orient) +'\" \n'
    S = S + 'graph [splines=' + str(splines) + '] \n'
    S = S + 'graph [ranksep=' + str(ranksep) + '] \n'
    S = S + 'graph [nodesep=' + str(nodesep) + '] \n'
    S = S + 'edge [arrowhead=' + str(arrowhead)+ '] \n'

    S = S + '\n'
    for i in range(len(mats)):
        if mats[i] in highlighted:
            S = S + graphviz_matrix_highlighted(i, mats[i].rows)
        else:
            S = S + graphviz_matrix(i, mats[i].rows)



    Relations = transitive_reduction(rels)

    for r in Relations:
        S = S + str(r[0]) + '->' + str(r[1]) + '\n'
    S = S + '\n }'
    return S
