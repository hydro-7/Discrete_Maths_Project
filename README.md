# Discrete Maths Project
Our group's Discrete Maths (CS-201) project submission. 

# Warshalls Algorithm Visualizer : 

For a Directed Graph, its Transitive Closure of a **Relation R** on a **Set A** is defined as the smallest **symmetric relation** that contains R. These transitive closures help to find the **Max Reachability** of the graph.

To calculate this Transitive Closure, we use the Warshall's Algorithm which has a **Time Complexity of :** `O(n^3)`.

# Features : 

- We used **Custom Tkinter** to build the dialogue boxes and **Networkx** to plot the graphical representations of the initial and final relations.
- The program takes in an input of Number of Vertices and the initial Relation. 
  - Sample Inputs : Number of Vertices : `4` and Edges : `{(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 0), (3, 3)}`
- The program produces a step by step process of how the algorithm works to get the final Transitive Closure and it also presents the Initial and Final directed graphs.


Images from the sample inputs :
![image](https://github.com/user-attachments/assets/92acd2de-87b0-4f08-861b-782d848963da)

![image](https://github.com/user-attachments/assets/8ecbc2d1-aaba-4ffd-8df5-b6b763e83875)


