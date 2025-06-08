A physics-based particle simulator built in Python using Pygame and NumPy. Particles interact using Newtonian gravity and can collide, merge, and leave fading trails. Features include real-time control over gravity, merging, and launching particles by click-dragging.

⸻

🚀 Features
    •    Realistic gravitational attraction (with optional repulsion toggle)
    •    Elastic or merging collisions
    •    Click-and-drag launching system
    •    Smooth trail rendering with fade
    •    Adjustable gravity strength (using up and down arrow keys)
    •    Pause/play, reset, and HUD display
    •    Fully documented and modular code

⸻

🧪 Physics Modeled
    •    Newton’s Law of Universal Gravitation:
F = G * (m₁ * m₂) / r²
    •    Elastic Collisions (conservation of momentum)
    •    Kinetic and Potential Energy Tracking

⸻

🎮 Controls
    •    Mouse drag and release: Launch a particle
    •    Spacebar: Pause or unpause the simulation
    •    G key: Toggle gravity between attraction and repulsion
    •    M key: Toggle merge-on-collision mode
    •    Up arrow key: Increase gravity strength
    •    Down arrow key: Decrease gravity strength

⸻

📦 Setup Instructions
    1.    Clone this repo
git clone https://github.com/your-username/gravity-simulator.git
cd gravity-simulator
    2.    Install dependencies
pip install -r requirements.txt
    3.    Run the simulator
python main.py

⸻

📂 Project Structure

gravity-simulator/
├── main.py         # Main simulation loop
├── particle.py     # Particle class: physics + rendering
├── physics.py      # Collision + energy functions
├── requirements.txt
└── README.md

⸻

📚 License

MIT License © 2025 Noam Pischanker
Feel free to modify, fork, or use for your own learning and portfolio projects!

⸻

🙌 Acknowledgements

Built with Python, NumPy, and Pygame. Inspired by orbital mechanics, educational physics tools, and chaos.
