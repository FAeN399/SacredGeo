def create_animation():
    """Create an animation of the Merkaba transforming and rotating"""
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # We'll animate rotation of the Merkaba
    num_frames = 48
    rotations = np.linspace(0, 2*np.pi, num_frames)
    
    def update(frame):
        ax.clear()
        rotation = rotations[frame]
        
        # Create Merkaba with current rotation
        merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=rotation)
        
        # Plot first tetrahedron
        tetra1 = merkaba['tetrahedron1']
        vertices1 = tetra1['vertices']
        faces1 = tetra1['faces']
        
        face_collection1 = []
        for face in faces1:
            face_vertices = [vertices1[i] for i in face]
            face_collection1.append(face_vertices)
        
        ax.add_collection3d(Poly3DCollection(
            face_collection1, 
            color='blue', 
            alpha=0.4, 
            linewidths=1,
            edgecolors='black'
        ))
        
        # Plot second tetrahedron
        tetra2 = merkaba['tetrahedron2']
        vertices2 = tetra2['vertices']
        faces2 = tetra2['faces']
        
        face_collection2 = []
        for face in faces2:
            face_vertices = [vertices2[i] for i in face]
            face_collection2.append(face_vertices)
        
        ax.add_collection3d(Poly3DCollection(
            face_collection2, 
            color='red', 
            alpha=0.4, 
            linewidths=1,
            edgecolors='black'
        ))
        
        # Add Vector Equilibrium outline if at π/4 rotation (optimal alignment)
        if np.isclose(rotation % np.pi, np.pi/4, atol=0.1):
            ve = create_cuboctahedron(center=(0, 0, 0), radius=1.0)
            ve_vertices = ve['vertices']
            for edge in ve['edges']:
                ax.plot3D([ve_vertices[edge[0]][0], ve_vertices[edge[1]][0]],
                          [ve_vertices[edge[0]][1], ve_vertices[edge[1]][1]],
                          [ve_vertices[edge[0]][2], ve_vertices[edge[1]][2]],
                          'gold', alpha=0.4, linewidth=2)
        
        ax.set_box_aspect([1, 1, 1])
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(-1.5, 1.5)
        ax.set_title(f"Merkaba Rotation - {rotation:.2f} radians")
        
        # Add note when at optimal alignment point
        if np.isclose(rotation % np.pi, np.pi/4, atol=0.1):
            plt.figtext(0.5, 0.02, "Optimal Alignment Point with Vector Equilibrium", ha='center', color='green')
        else:
            plt.figtext(0.5, 0.02, "", ha='center')
    
    ani = FuncAnimation(fig, update, frames=num_frames, interval=100, blit=False)
    plt.close()  # to prevent the static plot from displaying
    
    return HTML(ani.to_jshtml())

# Create and display the animation
create_animation()