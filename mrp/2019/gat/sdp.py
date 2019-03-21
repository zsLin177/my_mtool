from graph import Graph;

def read_matrix(file):
    rows = []
    for line in file:
        line = line.rstrip()
        if len(line) == 0:
            return rows
        else:
            rows.append(line.split("\t"))
    return None

def read_matrices(file):
    file.readline().rstrip()
    matrix = read_matrix(file)
    while matrix:
        yield matrix
        matrix = read_matrix(file)

def matrix2graph(matrix):
    graph = Graph(matrix[0][0][1:])
    predicates = []
    for id, row in enumerate(matrix[1:]):
        lemma, pos, frame, top = row[2], row[3], row[6], row[4] == '+'
        if lemma == "_": lemma = row[1]
        properties = {"pos": pos}
        if frame != "_": properties["frame"] = frame
        node = graph.add_node(id, label=lemma, properties=properties, top=top)
        if row[5] == '+':
            predicates.append(id)
    for tgt, row in enumerate(matrix[1:]):
        for pred, label in enumerate(row[7:]):
            if label != '_':
                src = predicates[pred]
                edge = graph.add_edge(src, tgt, label)
    return graph

def read_sdp(fp):
    for matrix in read_matrices(fp):
        yield matrix2graph(matrix)
