import re
from collections import deque
import functools
from itertools import zip_longest
from collections import Counter

import networkx as nx


class Pattern:
    def __init__(self, pattern):
        self.pattern = pattern
        self.next_special = {}

        self._init_next_special()

    def _init_next_special(self):
        search_pattern = re.compile(r'[$|()]')
        for i, c in enumerate(self.pattern):
            if c == '$':
                break
            m = search_pattern.search(self.pattern[i + 1:])
            assert i != m.start() + i + 1
            self.next_special[i] = m.start() + i + 1

    def __repr__(self):
        return f'{self.pattern}'


def create_all_paths(pattern: Pattern):

    paths = []
    i = 0
    stack = deque()
    current_path_index = None

    pattern_length = len(pattern.pattern)
    while i < pattern_length:
        if pattern.pattern[i] in 'NESW':
            i = handle_nesw(current_path_index, i, paths, pattern)
            continue
        elif pattern.pattern[i] == '(':
            i, current_path_index = handle_begin_branch(current_path_index, i, paths, pattern, stack)
            continue
        elif pattern.pattern[i] == '|':
            i = handle_choice(i, pattern)
            continue
        elif pattern.pattern[i] == ')':
            #i = handle_end_branch(i)
            i += 1
            continue
        elif pattern.pattern[i] == '$':
            if len(stack):
                if current_path_index != len(paths) - 1:
                    print(current_path_index, len(paths))
                # assert current_path_index == len(paths) - 1
                yield paths.pop()
                orig_current_path_index = current_path_index
                i, current_path_index = end_fix_stack(stack, current_path_index)
                # assert orig_current_path_index == current_path_index + 1
                # assert pattern.pattern[i] != '$'
                # print(len(stack))
                continue
            else:
                yield paths.pop(current_path_index)
                return
        elif pattern.pattern[i] == '^':
            i, current_path_index = handle_begin(paths, i)
            continue
        return


class CreateAllPaths2:

    def __init__(self, pattern: Pattern):
        self.pattern = pattern
        self.paths = []
        self.stack = deque()
        self.already = set()
        self.graph = nx.Graph()
        self.current_path_index = None

    def handle_nesw2(self, i):
        #assert self.current_path_index == 0
        edges = set()
        j = 0
        orig_stack_len = len(self.stack)
        while j < len(self.stack):
            pattern_index, paths_index = self.stack.popleft()
            assert paths_index != self.current_path_index
            if paths_index == self.current_path_index:
                continue
            if pattern_index == i:
                y, x = self.paths[paths_index]
                if pattern_index >= len(self.pattern.pattern[pattern_index]) - 1:
                    continue
                if (y, x, i) not in self.already:
                    self.already.add((y, x, i))
                    extra_edges, x, y = self.create_edges(i, x, y)
                    edges.update(extra_edges)
                    self.paths[paths_index] = (y, x)
                else:
                    del self.paths[paths_index]
                    k = 0
                    while k < len(self.stack):
                        d1, d2 = self.stack.popleft()
                        if d2 > paths_index:
                            self.stack.append((d1, d2 - 1))
                        else:
                            self.stack.append((d1, d2))
                        k += 1
                    continue
                pattern_index += self.pattern.next_special[i]
            self.stack.append((pattern_index, paths_index))
            j += 1

        y, x = self.paths[self.current_path_index]
        extra_edges, x, y = self.create_edges(i, x, y)
        edges.update(extra_edges)
        self.graph.add_edges_from(edges)
        self.paths[self.current_path_index] = (y, x)
        return self.pattern.next_special[i]

    @functools.lru_cache(maxsize=1000000)
    def create_edges(self, i, x, y):
        edges, rel_x, rel_y = self.create_edges_relative(i)
        edges = {((n1[0] + y, n1[1] + x), (n2[0] + y, n2[1] + x)) for (n1, n2) in edges}
        return edges, x + rel_x, y + rel_y

    def create_edges_relative(self, i):
        edges = set()
        rel_y, rel_x = 0, 0
        for c in self.pattern.pattern[i:self.pattern.next_special[i]]:
            old_y, old_x = rel_y, rel_x
            if c == 'N':
                rel_y += 1
            elif c == 'S':
                rel_y -= 1
            elif c == 'E':
                rel_x -= 1
            elif c == 'W':
                rel_x += 1
            edges.add(((old_y, old_x), (rel_y, rel_x)))
        return edges, rel_x, rel_y

    def handle_begin_branch2(self, i):
        # First we want to process the first choice
        y, x = self.paths[self.current_path_index]
        new_paths = [(i + 1, (self.current_path_index))]
        # Now we want to process the remaining choices
        current_depth = 0
        while True:
            i = self.pattern.next_special[i]
            if self.pattern.pattern[i] == '(':
                current_depth += 1
            elif self.pattern.pattern[i] == ')':
                current_depth -= 1
                if current_depth < 0:
                    break
            elif self.pattern.pattern[i] == '|':
                if current_depth == 0:
                    self.paths.append((y, x))
                    current_path_index = len(self.paths) - 1
                    new_paths.append((i + 1, current_path_index))
        self.stack.extend(list(reversed(new_paths)))
        return self.stack.pop()

    def end_fix_stack2(self):
        i = 0
        while i < len(self.stack):
            pattern_index, path_index = self.stack.pop()
            if path_index >= self.current_path_index:
                self.stack.appendleft((pattern_index, path_index - 1))
                i += 1
            else:
                self.stack.appendleft((pattern_index, path_index))
                i += 1
        return self.stack.popleft()

    @functools.lru_cache()
    def handle_choice2(self, i):
        # We are done with this choice, we want to skip to the ')' that matches our current depth
        current_depth = 0
        while True:
            i = self.pattern.next_special[i]
            if self.pattern.pattern[i] == '(':
                current_depth += 1
            elif self.pattern.pattern[i] == ')':
                current_depth -= 1
                if current_depth < 0:
                    break
        return i

    def create_all_paths2(self):

        i = 0
        max_nodes = 0

        pattern_length = len(self.pattern.pattern)
        while i < pattern_length:
            if self.pattern.pattern[i] in 'NESW':
                i = self.handle_nesw2(i)
                continue
            elif self.pattern.pattern[i] == '(':
                i, self.current_path_index = self.handle_begin_branch2(i)
                continue
            elif self.pattern.pattern[i] == '|':
                i = self.handle_choice2(i)
                continue
            elif self.pattern.pattern[i] == ')':
                i += 1
                continue
            elif self.pattern.pattern[i] == '$':
                if len(self.stack):
                    #assert self.current_path_index == len(self.paths) - 1
                    #yield paths.pop()
                    self.paths.pop(self.current_path_index)
                    if len(self.graph.nodes) > max_nodes:
                        max_nodes = len(self.graph.nodes)
                        yield self.graph
                    orig_current_path_index = self.current_path_index
                    #for x in stack:
                    #    assert len(x) == 2
                    i, self.current_path_index = self.end_fix_stack2()
                    # assert orig_current_path_index == current_path_index + 1
                    # assert pattern.pattern[i] != '$'
                    continue
                else:
                    #yield paths.pop(current_path_index)
                    self.paths.pop(self.current_path_index)
                    yield self.graph
                    if len(self.graph.nodes) > max_nodes:
                        max_nodes = len(self.graph.nodes)
                        yield self.graph
                    return
            elif self.pattern.pattern[i] == '^':
                self.paths = [(0, 0)]
                i, self.current_path_index = i + 1, 0
                continue


def end_fix_stack(stack, current_path_index):
    if not (current_path_index == len(stack)):
        print(current_path_index, len(stack))
    #assert current_path_index == len(stack)
    for j, s in enumerate(reversed(stack)):
        if s[1] > current_path_index:
            stack[len(stack) - j] = (s[0], s[1] - 1)
        else:
            break
    return stack.pop()


def handle_end_branch(i):
    return i + 1


def handle_choice(i, pattern: Pattern):
    # We are done with this choice, we want to skip to the ')' that matches our current depth
    current_depth = 0
    while True:
        i = pattern.next_special[i]
        if pattern.pattern[i] == '(':
            current_depth += 1
        elif pattern.pattern[i] == ')':
            current_depth -= 1
            if current_depth < 0:
                break
    return i


def handle_begin_branch(current_path_index, i, paths, pattern: Pattern, stack):
    # First we want to process the first choice
    current_path = paths[current_path_index]
    new_paths = [(i + 1, current_path_index)]
    # Now we want to process the remaining choices
    current_depth = 0
    while True:
        i = pattern.next_special[i]
        if pattern.pattern[i] == '(':
            current_depth += 1
        elif pattern.pattern[i] == ')':
            current_depth -= 1
            if current_depth < 0:
                break
        elif pattern.pattern[i] == '|':
            if current_depth == 0:
                paths.append('' + current_path)
                current_path_index = len(paths) - 1
                new_paths.append((i + 1, current_path_index))
    #print(f'Extending stack with {list(reversed(new_paths))}')
    stack.extend(new_paths)
    return stack.pop()


def handle_nesw(current_path_index, i, paths, pattern: Pattern):
    paths[current_path_index] = paths[current_path_index] + pattern.pattern[i:pattern.next_special[i]]
    return pattern.next_special[i]


def handle_begin(paths, i):
    paths.append('')
    return i + 1, 0


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


@functools.lru_cache(maxsize=1000000)
def add_nodes(g, path, y=0, x=0):
    if len(path) <= 0:
        return y, x
    if len(path) <= 5:
        for c in path:
            old_y, old_x = y, x
            if c == 'N':
                y -= 1
            if c == 'W':
                x -= 1
            if c == 'S':
                y += 1
            if c == 'E':
                x += 1
            g.add_edge((old_y, old_x), (y, x))
        return y, x
    y, x = add_nodes(g, path[:len(path)//2], y, x)
    return add_nodes(g, path[len(path)//2:], y, x)


grouped_path_segments = {}


def add_nodes_orig(g, path):
    global grouped_path_segments
    y, x = 0, 0
    for segment50 in grouper(path, 50):
        if (y, x, segment50) in grouped_path_segments:
            y, x = grouped_path_segments[(y, x, segment50)]
        else:
            orig50_y, orig50_x = y, x
            for segment10 in grouper(segment50, 10):
                if (y, x, segment10) in grouped_path_segments:
                    y, x = grouped_path_segments[(y, x, segment10)]
                else:
                    orig10_y, orig10_x = y, x
                    for c in segment10:
                        old_y, old_x = y, x
                        if c == 'N':
                            y -= 1
                        if c == 'W':
                            x -= 1
                        if c == 'S':
                            y += 1
                        if c == 'E':
                            x += 1
                        g.add_edge((old_y, old_x), (y, x))
                    grouped_path_segments[(orig10_y, orig10_x, segment10)] = (y, x)
            grouped_path_segments[(orig50_y, orig50_x, segment50)] = (y, x)


def part1(data):
    g = nx.Graph()
    paths_index = 0
    for path in create_all_paths(Pattern(data)):
        add_nodes(g, path)
        paths_index += 1

    shortest_paths = nx.single_source_shortest_path(g, (0, 0))
    gt_1000 = 0
    max_path = 0
    for key in shortest_paths:
        if len(shortest_paths[key]) - 1 >= 1000:
            gt_1000 += 1
        if len(shortest_paths[key]) - 1 > max_path:
            max_path = len(shortest_paths[key]) - 1
    return max_path


def part2(data):
    paths_index = 0
    o = CreateAllPaths2(Pattern(data))
    g = None
    for g in o.create_all_paths2():
        pass

    shortest_paths = nx.single_source_shortest_path(g, (0, 0))
    print(f'Total nodes: {len(g.nodes)}')
    gt_1000 = 0
    for key in shortest_paths:
        if len(shortest_paths[key]) - 1 >= 1000:
            gt_1000 += 1
    return gt_1000


def remove_loops(data):
    search_pattern = re.compile(r'[$|()]')
    orig_len = len(data)
    replacements = [1]
    while replacements:
        replacements = []
        for i, c in enumerate(data):
            if c == '$':
                break
            if c in '()|^':
                m = search_pattern.search(data[i + 1:])
                if not m:
                    print(data[i + 1:])
                    continue
                if m.start() == 0:
                    continue
                next_special_index = m.start() + i + 1
                assert i != next_special_index
                assert i + 1 != next_special_index
                assert '|' not in data[i + 1:next_special_index]
                assert '(' not in data[i + 1:next_special_index]
                assert ')' not in data[i + 1:next_special_index]
                assert '$' not in data[i + 1:next_special_index]
                counter = Counter(data[i + 1:next_special_index])
                if counter.get('N', 0) == counter.get('S', 0):
                    if counter.get('W', 0) == counter.get('E', 0):
                        replacements.append((i + 1, next_special_index))

        for start, end in reversed(replacements):
            data = data[0:start] + data[end:]

    data = data.replace('(|)', '')
    return data


def get_data():
    with open('input20.txt') as f:
        data = f.read().rstrip('\n')
    re.compile(data)
    return data


def find_max_depth(data):
    depth = 0
    max_depth = 0
    max_depth_index = 0
    for i, c in enumerate(data):
        if c == '(':
            depth += 1
            if max_depth < depth:
                max_depth = depth
                max_depth_index = i
        if c == ')':
            depth -= 1
    return max_depth_index, max_depth



if __name__ == '__main__':
    data = get_data()
    data = remove_loops(data)
    part1_answer = part1(data)
    print(f'Day 20 Part 1 Answer: {part1_answer}')
    data = get_data()
    part2_answer = part2(data)
    print(f'Day 20 Part 1 Answer: {part2_answer}')
