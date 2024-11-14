import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt

def parse_edges(input_str, n):
    edges = eval(input_str)  # Example input: {(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 0), (3, 3)}
    graph = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        graph[u][v] = 1  
    
    return graph

def warshall_algorithm(graph, n):
    output_matrices = [] 
    reach = [row[:] for row in graph] 
    
    output_matrices.append(format_matrix(reach, n))
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
        
       
        output_matrices.append(format_matrix(reach, n))
    
    return output_matrices, reach 

def format_matrix(matrix, n):
    result = ""
    for row in matrix:
        result += ' '.join(map(str, row)) + "\n"
    return result

def get_edges_dialog(n):
    edges_dialog = ctk.CTkToplevel(root)
    edges_dialog.title("Enter Graph Edges")
    edges_dialog.geometry("500x400")
    
    edges_dialog.focus_force()
    edges_dialog.grab_set()
    
    instruction_label = ctk.CTkLabel(edges_dialog, text="Enter the edges in the format {(u, v), (x, y), ...}", font=("Arial", 14))
    instruction_label.pack(pady=10)

    edges_entry = ctk.CTkEntry(edges_dialog, width=400, height=40, placeholder_text="{(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 0), (3, 3)}")
    edges_entry.pack(pady=10)

    error_label = ctk.CTkLabel(edges_dialog, text="", text_color="red")
    error_label.pack(pady=5)

   
    edges_result = []

    def confirm_edges():
        input_str = edges_entry.get().replace('\u00A0', ' ')  
        try:
            edges = eval(input_str)
            if not isinstance(edges, set):
                raise ValueError("Input should be a set of tuples")
            for u, v in edges:
                if u < 0 or u >= n or v < 0 or v >= n:
                    raise ValueError("Vertices out of range")
            edges_result.append(input_str)  
            edges_dialog.destroy()  
        except Exception as e:
            error_label.configure(text=f"Invalid input: {str(e)}")  
    
   
    confirm_button = ctk.CTkButton(edges_dialog, text="Confirm", command=confirm_edges)
    confirm_button.pack(pady=20)

    edges_dialog.wait_window(edges_dialog) 
    return edges_result[0] if edges_result else None 


def draw_graph_from_matrix(matrix, n, ax, title):
    G = nx.DiGraph()
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                G.add_edge(i, j)
    
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=700, node_color='lightblue', font_size=16, font_weight='bold', ax=ax)
    ax.set_title(title)

# Real Func
def run_algorithm():
    
    dialog = ctk.CTkToplevel(root)
    dialog.title("Input Required")
    dialog.geometry("400x300")  

    dialog.focus_force()
    dialog.grab_set()  
    
    n_label = ctk.CTkLabel(dialog, text="Enter the number of vertices:", font=("Arial", 14))
    n_label.pack(pady=10)
    
    n_entry = ctk.CTkEntry(dialog, width=250)
    n_entry.pack(pady=10)

    error_label = ctk.CTkLabel(dialog, text="", text_color="red")
    error_label.pack(pady=5)
    
    def confirm_vertices():
        try:
            n = int(n_entry.get())
            if n <= 0:
                raise ValueError("Number of vertices must be positive.")
        except ValueError:
            error_label.configure(text="Invalid input. Please enter a positive integer.")
            return
        
        dialog.destroy()  

        input_str = get_edges_dialog(n)
        if input_str is None:
            return  

        graph = parse_edges(input_str, n)
        output_matrices, final_reach = warshall_algorithm(graph, n)

        
        output_window = ctk.CTkToplevel(root)
        output_window.title("Algorithm Output")
        output_window.geometry("900x600")  
        
        output_frame = ctk.CTkFrame(output_window)
        output_frame.pack(pady=10, fill="both", expand=True)  
        
        matrix_frame = ctk.CTkFrame(output_frame)
        matrix_frame.pack(pady=10)  
        
        matrix_frames = []
        
        center_frame = ctk.CTkFrame(matrix_frame)
        center_frame.pack(side="top", fill="both", expand=True)

        for i, matrix_output in enumerate(output_matrices):
            frame = ctk.CTkFrame(center_frame, width=220, height=220)  
            frame.pack(side="left", padx=5, pady=5) 
            
            label = ctk.CTkLabel(frame, text=matrix_output, anchor="center", justify="center", font=("Arial", 24))  
            label.pack(side="top", fill="both", expand=True)  
            
            matrix_frames.append(frame)

            if i < len(output_matrices) - 1:
                arrow_label = ctk.CTkLabel(center_frame, text="→", font=("Arial", 24))  
                arrow_label.pack(side="left")  

        ordered_pairs = []
        for i in range(len(final_reach)):
            for j in range(len(final_reach)):
                if final_reach[i][j] == 1:
                    ordered_pairs.append(f"({i}, {j})")

        pairs_label = ctk.CTkLabel(output_frame, text="Ordered Pairs (Edges) of the Transitive Closure:", font=("Arial", 16))
        pairs_label.pack()

        edges_label = ctk.CTkLabel(output_frame, text=", ".join(ordered_pairs), font=("Arial", 16), anchor="center")
        edges_label.pack(pady=10)  

        
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))  

        
        draw_graph_from_matrix(graph, n, axs[0], "Input Matrix Graph")
        
        
        draw_graph_from_matrix(final_reach, n, axs[1], "Final Reachability Graph")

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)  
        plt.show()  

        
        for frame in matrix_frames:
            frame.configure(width=max(frame.winfo_width() for frame in matrix_frames), height=max(frame.winfo_height() for frame in matrix_frames))

        matrix_frame.pack(expand=True)

    confirm_button = ctk.CTkButton(dialog, text="Confirm", command=confirm_vertices)
    confirm_button.pack(pady=20)

root = ctk.CTk() 
root.geometry("400x300")
root.title("Warshall's Algorithm")

button = ctk.CTkButton(root, text="Run Warshall's Algorithm", command=run_algorithm)
button.pack(pady=50)

root.mainloop() # Start the Tkinter main loop

