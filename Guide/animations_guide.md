# Working with Sacred Geometry Animations

This guide covers how to create and customize animations in the Advanced Sacred Geometry project.

## Available Animations

### 1. Merkaba Animations (merkaba_animations.py)
- **Rotation Animation**: Full 3D rotation of the Merkaba
- **Energy Pulse**: Visualization of energy flow between tetrahedra
- Customizable colors, speeds, and transitions

### 2. General Animations (example_animations.py)
- **Flower of Life Growth**: Progressive expansion of the pattern
- **Sacred Spiral**: Unwinding golden ratio spiral
- **Metatron's Cube Rotation**: 2D rotation with depth perception
- **Koch Snowflake Evolution**: Fractal generation process

## Creating Animations

### Basic Animation Structure
```python
def create_animation(num_frames=60):
    fig = plt.figure(figsize=(10, 10))
    ax = setup_axes()  # Configure your axes
    
    def update(frame):
        ax.clear()
        # Your frame-by-frame drawing code here
        return ax,
    
    anim = animation.FuncAnimation(
        fig, update, frames=num_frames,
        interval=50, blit=False
    )
    return anim
```

### Animation Parameters

1. **Frame Control**:
   - `num_frames`: Total number of frames
   - `interval`: Milliseconds between frames
   - `blit`: Set False for 3D animations

2. **Quality Settings**:
   - `fps`: Frames per second in saved file
   - `dpi`: Resolution of output
   - `writer`: 'pillow' for GIF, 'ffmpeg' for MP4

### Tips for Smooth Animations

1. **Performance**:
   - Clear axes each frame
   - Minimize object creation
   - Use appropriate number of frames
   - Consider lower resolution for testing

2. **Memory Management**:
   - Close figures after saving
   - Clear unused variables
   - Use appropriate data types

3. **Visual Quality**:
   - Add smooth transitions
   - Include ease-in/ease-out
   - Maintain consistent frame rate

## Example Customizations

### 1. Merkaba Rotation
```python
animate_merkaba_rotation(
    num_frames=72,      # Smooth 360° rotation
    elevation_change=True  # Add vertical motion
)
```

### 2. Sacred Spiral
```python
animate_sacred_spiral(
    num_frames=60,
    turns=8,
    color_gradient=True
)
```

### 3. Flower of Life
```python
animate_flower_growth(
    num_frames=60,
    fade_in=True,
    color_shift=True
)
```

## Output Formats

### 1. GIF Animation
```python
anim.save('animation.gif',
    writer='pillow',
    fps=15,
    dpi=150
)
```

### 2. MP4 Video (requires ffmpeg)
```python
anim.save('animation.mp4',
    writer='ffmpeg',
    fps=30,
    dpi=300
)
```

### 3. HTML5 (for Jupyter)
```python
HTML(anim.to_jshtml())
```

## Advanced Techniques

### 1. Multi-Object Animation
- Track multiple objects independently
- Synchronize movements
- Handle object interactions

### 2. Complex Transitions
- Use easing functions
- Implement morphing between shapes
- Create particle effects

### 3. Interactive Animations
- Add pause/play controls
- Include parameter sliders
- Enable real-time adjustments

## Troubleshooting

### Common Issues

1. **Choppy Animation**:
   - Reduce complexity of each frame
   - Lower the frame rate
   - Simplify geometries

2. **Memory Errors**:
   - Reduce number of frames
   - Clear figures after saving
   - Use appropriate data types

3. **Export Problems**:
   - Check writer availability
   - Verify file permissions
   - Monitor available disk space

## Best Practices

1. **Planning**:
   - Sketch animation sequence
   - Define key frames
   - Test with low resolution

2. **Development**:
   - Start simple, add complexity
   - Test frequently
   - Version your changes

3. **Optimization**:
   - Profile performance
   - Cache repeated calculations
   - Use vectorized operations

## Resources

- Matplotlib Animation API
- Sacred Geometry example scripts
- Animation output directory structure
- Reference implementations