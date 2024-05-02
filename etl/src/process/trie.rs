//! prefix tree

use std::{collections::BTreeMap, ops::Deref};

#[derive(Default)]
pub struct Tree {
    root: Node,
}

impl Tree {
    pub fn insert(&mut self, s: &str) {
        self.root.occur += 1;

        let mut cur = &mut self.root;
        for i in s.chars() {
            cur = cur.add_child(i);
            cur.occur += 1;
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
    pub fn iter(&self) -> TreeIter {
        let mut stack = Vec::new();

        for (i, child) in self.root.children.iter() {
            stack.push((child.deref(), *i, 0));
        }

        TreeIter {
            prefix: String::new(),
            stack,
        }
    }
}

impl FromIterator<String> for Tree {
    fn from_iter<I: IntoIterator<Item = String>>(iter: I) -> Self {
        let mut tree = Tree::default();
        for i in iter {
            tree.insert(&i);
        }
        tree
    }
}

pub struct TreeIter<'a> {
    prefix: String,
    stack: Vec<(&'a Node, char, usize)>,
}

impl Iterator for TreeIter<'_> {
    type Item = (usize, String);

    fn next(&mut self) -> Option<Self::Item> {
        while let Some((node, c, depth)) = self.stack.pop() {
            self.prefix.truncate(depth);
            self.prefix.push(c);
            for (i, child) in node.children.iter() {
                self.stack.push((node, *i, depth + 1));
                if child.leaf {
                    return Some((child.occur, self.prefix.clone()));
                }
            }
        }
        None
    }
}

#[derive(Default)]
struct Node {
    children: BTreeMap<char, Box<Node>>,
    occur: usize,
    leaf: bool,
}

impl Node {
    fn add_child(&mut self, i: char) -> &mut Self {
        self.children
            .entry(i)
            .or_insert_with(|| Box::new(Node::default()))
    }
}
