"""
Example script demonstrating Merkaba (Star Tetrahedron) animations.
This shows the sacred Merkaba rotating in 3D space with different viewing angles.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Ensure 3D projection is available
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sacred_geometry.shapes.shapes import create_merkaba

# Create output directory if it doesn't exist
output_dir = "examples/outputs/animations"
os.makedirs(output_dir, exist_ok=True)

def animate_merkaba_rotation(num_frames=120, elevation_change=True):
    """
    Animate a Merkaba (Star Tetrahedron) rotating in 3D space.
    
    Parameters:
    - num_frames: Number of frames in the animation
    - elevation_change: If True, also changes the viewing elevation during animation
    """
    # Create figure for 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Rotating Merkaba (Star Tetrahedron)")
    
    # Set axis limits
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    
    # Remove axis labels for clean visualization
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    
    # Create basic Merkaba
    merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=0)
    
    # Extract vertices and faces from both tetrahedra
    vertices1 = np.array(merkaba['tetrahedron1']['vertices'])
    faces1 = merkaba['tetrahedron1']['faces']
    vertices2 = np.array(merkaba['tetrahedron2']['vertices'])
    faces2 = merkaba['tetrahedron2']['faces']
    
    # Combine vertices; update faces for the second tetrahedron accordingly
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + [(f[0]+len(vertices1), f[1]+len(vertices1), f[2]+len(vertices1)) for f in faces2]
    
    # Colors for the two tetrahedra (assume first half faces from tetrahedron1, second half from tetrahedron2)
    colors = ['#1f77b4', '#ff7f0e']  # Blue and orange
    
    def update(frame):
        ax.clear()
        
        # Set title, limits, and remove tick labels
        ax.set_title("Rotating Merkaba (Star Tetrahedron)")
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(-1.5, 1.5)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        
        # Calculate rotation angles based on frame
        theta = frame / num_frames * 2 * np.pi  # Full rotation around Z
        phi = frame / num_frames * np.pi          # Half rotation around X
        
        # Create rotation matrices
        Rz = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0,              0,             1]
        ])
        Rx = np.array([
            [1, 0,             0],
            [0, np.cos(phi),  -np.sin(phi)],
            [0, np.sin(phi),   np.cos(phi)]
        ])
        R = np.dot(Rz, Rx)
        
        # Apply rotation to vertices
        rotated_vertices = np.dot(vertices, R.T)
        
        # Set view angle if elevation change is enabled
        if elevation_change:
            elevation = 30 + 20 * np.sin(frame / num_frames * 2 * np.pi)
            azimuth = (frame / num_frames * 360) % 360
            ax.view_init(elev=elevation, azim=azimuth)
        else:
            azimuth = (frame / num_frames * 360) % 360
            ax.view_init(elev=30, azim=azimuth)
        
        # Prepare polygons for faces
        poly3d_faces = []
        face_colors = []
        for i, face in enumerate(faces):
            # Get the vertices for this face
            face_verts = [rotated_vertices[idx].tolist() for idx in face]
            poly3d_faces.append(face_verts)
            # Assign color based on the tetrahedron (first half for tetrahedron1, second half for tetrahedron2)
            if i < len(faces) // 2:
                face_colors.append(colors[0])
            else:
                face_colors.append(colors[1])
        
        # Create a 3D polygon collection and add to the axis
        poly3d = Poly3DCollection(poly3d_faces, facecolors=face_colors, linewidths=1, edgecolors='black', alpha=0.7)
        ax.add_collection3d(poly3d)
        
        return ax,
    
    # Create animation (set blit=False for 3D animations)
    anim = animation.FuncAnimation(
        fig, update, frames=num_frames, interval=50, blit=False
    )
    
    # Save animation (GIF format)
    filename = os.path.join(output_dir, "merkaba_rotation_3d.gif")
    anim.save(filename, writer='pillow', fps=20)
    print(f"Saved: {filename}")
    plt.close(fig)

def animate_merkaba_pulse(num_frames=90):
    """
    Animate a Merkaba with pulsating energy between the two tetrahedra.
    """
    # Create figure for 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Pulsating Merkaba Energy")
    
    # Set axis limits
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    
    # Remove axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    
    # Create basic Merkaba
    merkaba = create_merkaba(center=(0, 0, 0), radius=1.0, rotation=np.pi/7)
    
    # Extract vertices and faces from both tetrahedra
    vertices1 = np.array(merkaba['tetrahedron1']['vertices'])
    faces1 = merkaba['tetrahedron1']['faces']
    vertices2 = np.array(merkaba['tetrahedron2']['vertices'])
    faces2 = merkaba['tetrahedron2']['faces']
    
    # Animation function
    def update(frame):
        ax.clear()
        
        # Set title and limits for each frame
        ax.set_title("Pulsating Merkaba Energy")
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(-1.5, 1.5)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        
        # Calculate energy phase (oscillating between tetrahedra)
        energy_phase = np.sin(frame / num_frames * 2 * np.pi)
        
        # Calculate colors based on energy phase
        # When energy_phase is positive, first tetrahedron is more energized
        # When energy_phase is negative, second tetrahedron is more energized
        alpha1 = 0.4 + 0.5 * max(0, energy_phase)  # First tetrahedron
        alpha2 = 0.4 + 0.5 * max(0, -energy_phase)  # Second tetrahedron
        
        # Set the view angle - slow rotation
        azimuth = (frame / num_frames * 180) % 360  # Half speed rotation
        ax.view_init(elev=30, azim=azimuth)
        
        # First tetrahedron - calculate glow effect
        glow_size1 = 1.0 + 0.1 * max(0, energy_phase)  # Slight size increase when energized
        color1 = '#3498db'  # Blue
        scaled_vertices1 = vertices1 * glow_size1
        
        # Draw first tetrahedron using Poly3DCollection
        poly_faces1 = []
        for face in faces1:
            # Get the vertices for this face
            face_verts = [scaled_vertices1[idx].tolist() for idx in face]
            poly_faces1.append(face_verts)
        
        # Create polygon collection for first tetrahedron
        poly1 = Poly3DCollection(poly_faces1, facecolors=color1, linewidths=1, 
                                edgecolors='black', alpha=alpha1)
        ax.add_collection3d(poly1)
        
        # Second tetrahedron - calculate glow effect
        glow_size2 = 1.0 + 0.1 * max(0, -energy_phase)  # Slight size increase when energized
        color2 = '#e74c3c'  # Red
        scaled_vertices2 = vertices2 * glow_size2
        
        # Draw second tetrahedron using Poly3DCollection
        poly_faces2 = []
        for face in faces2:
            # Get the vertices for this face
            face_verts = [scaled_vertices2[idx].tolist() for idx in face]
            poly_faces2.append(face_verts)
        
        # Create polygon collection for second tetrahedron
        poly2 = Poly3DCollection(poly_faces2, facecolors=color2, linewidths=1, 
                                edgecolors='black', alpha=alpha2)
        ax.add_collection3d(poly2)
        
        return ax,
    
    # Create animation (using blit=False for 3D animations)
    anim = animation.FuncAnimation(
        fig, update, frames=num_frames, interval=50, blit=False
    )
    
    # Save animation
    filename = os.path.join(output_dir, "merkaba_pulsating.gif")
    anim.save(filename, writer='pillow', fps=15)
    print(f"Saved: {filename}")
    plt.close(fig)

# Run animations when script is executed directly
if __name__ == "__main__":
    print("Generating Merkaba animations...")
    animate_merkaba_rotation(num_frames=72)
    animate_merkaba_pulse(num_frames=60)
    print("Merkaba animations generated successfully.")