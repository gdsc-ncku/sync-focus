//! prefix tree

use std::collections::BTreeMap;

#[derive(Default)]
pub struct Tree<V: Default> {
    root: Node<V>,
}

impl<V: Default> Tree<V> {
    pub fn insert(&mut self, s: &str, mut f: impl FnMut(&mut V)) {
        f(&mut self.root.data);

        let mut cur = &mut self.root;
        for i in s.chars() {
            cur = cur.add_child(i);
            f(&mut cur.data);
        }
        cur.leaf = true;
    }
    // pub fn is_empty(&self) -> bool {
    //     self.root.occur == 0
    // }
    // pub fn len(&self) -> usize {
    //     self.root.occur
    // }
    // pub fn extend(&mut self, other: impl Iterator<Item = String>) {
    //     for prefix in other {
    //         self.insert(&prefix);
    //     }
    // }
    // pub fn from_iter<I: IntoIterator<Item = String>>(
    //     iter: I,
    //     mut f: impl FnMut(&mut V, &str),
    // ) -> Self {
    //     let mut tree = Tree::default();
    //     for i in iter {
    //         // tree.insert(&i, f);
    //     }
    //     tree
    // }
    pub fn into_iter(self) -> TreeIter<V> {
        let mut stack = Vec::new();

        for (i, child) in self.root.children.into_iter() {
            stack.push((child, i, 0));
        }

        TreeIter {
            prefix: String::new(),
            stack,
        }
    }
}

pub struct TreeIter<V: Default> {
    prefix: String,
    stack: Vec<(Box<Node<V>>, char, usize)>,
}

impl<V: Default> Iterator for TreeIter<V> {
    type Item = (String, V);

    fn next(&mut self) -> Option<Self::Item> {
        while let Some((node, c, depth)) = self.stack.pop() {
            self.prefix.truncate(depth);
            self.prefix.push(c);
            let data = (self.prefix.clone(), node.data);
            for (i, child) in node.children.into_iter() {
                self.stack.push((child, i, depth + 1));
            }
            if node.leaf {
                return Some(data);
            }
        }
        None
    }
}

#[derive(Default)]
struct Node<V: Default> {
    children: BTreeMap<char, Box<Node<V>>>,
    data: V,
    leaf: bool,
}

impl<V: Default> Node<V> {
    fn add_child(&mut self, i: char) -> &mut Self {
        self.children
            .entry(i)
            .or_insert_with(|| Box::new(Node::default()))
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn trie_iter() {
        let mut tree = Tree::<i32>::default();
        tree.insert("hello", |x| *x += 1);
        tree.insert("world", |x| *x += 1);
        assert_eq!(
            [("world".to_string(), 1_i32), ("hello".to_string(), 1_i32)],
            *tree.into_iter().collect::<Vec<_>>()
        );
    }
    #[test]
    fn test_not_dfs() {
        let mut tree = Tree::<i32>::default();
        tree.insert("hello", |x| *x += 1);
        tree.insert("helloaaa", |x| *x += 1);
        tree.insert("helloaaabb", |x| *x += 1);
        assert_eq!(
            [
                ("hello".to_string(), 3_i32),
                ("helloaaa".to_string(), 2_i32),
                ("helloaaabb".to_string(), 1_i32)
            ],
            *tree.into_iter().collect::<Vec<_>>()
        );
    }
}
