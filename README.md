# Real-Time-CV-Halide

## Project Structure and Development Plan: Real-time Interactive Video Filter

The core idea is to build layers, starting with the basics, then adding the advanced components. At each stage, measure performance to quantify your improvements.

---

### Phase 1: Foundation - Basic Video Stream & Non-Optimized Filters (Python)

**Goal:** Get the core video capture and display working, and implement a few simple filters in a non-optimized way to establish a performance baseline.

#### 1. Setup Environment
- Create a dedicated Python virtual environment (e.g., using `venv` or `conda`).
- Install necessary libraries: `opencv-python`, `numpy`.

#### 2. Basic Webcam Stream
- Write a Python script to capture frames from your webcam.
- Display the frames in a window in real-time.
- Add a way to exit the application gracefully (e.g., pressing 'q').

#### 3. Simple Filters (Non-Optimized)
- Implement 2-3 basic image filters using only NumPy array operations initially (no `cv2` for the filter logic itself, to simulate a "from-scratch" approach for later comparison).
    - **Example:** Grayscale conversion, simple manual blur (e.g., averaging 3x3 neighbors with explicit loops for a very baseline comparison to highly optimized `cv2` or Halide later), pixelation (manual resize/nearest neighbor).
- Apply these filters to the entire frame.

#### 4. Initial Performance Measurement
- Measure the Frames Per Second (FPS) of the raw video stream.
- Measure the FPS when each filter is applied (this will likely be very low for NumPy-only filters). This is your baseline for optimization.

**Output of Phase 1:**
A Python script showing live webcam feed with selectable, non-optimized filters applied globally.

---

### Phase 2: Hand/Gesture Detection & ROI Definition (Python & MediaPipe)

**Goal:** Accurately detect your hand/finger in real-time and define the region of interest (ROI) where filters will be applied.

#### 1. Integrate MediaPipe Hands
- Install `mediapipe`.
- Modify your Python script to use `mediapipe.solutions.hands` to detect hands and extract keypoints from each frame.
- Overlay the detected hand landmarks on your video feed for visualization and debugging.

#### 2. Finger Position & ROI
- From the detected keypoints, identify the coordinates of a specific fingertip (e.g., index finger).
- Define a dynamic ROI (e.g., a circle or square of a fixed size) around this fingertip's coordinates.
- Draw a visual indicator (circle/square) on the frame to show the current ROI.

#### 3. Basic Gesture Mapping
- Implement simple logic to detect one or two basic gestures (e.g., just the presence of a specific finger, or a "fist" vs. "open hand").
- Map these gestures to trigger specific filters. Initially, just print which filter is activated.

**Output of Phase 2:**
Live webcam feed showing hand/finger tracking, a visible ROI following the finger, and console output indicating detected gestures/activated filters.

---

### Phase 3: Localized Filtering & Python-Level Optimization

**Goal:** Apply filters only to the ROI, optimize these operations within Python, and measure the performance improvement.

#### 1. Localized Filter Application
- Modify your filter functions to apply only to the defined ROI. This often involves:
    - Cropping the ROI from the main frame.
    - Applying the filter to the cropped ROI.
    - Pasting the processed ROI back onto the original frame.
    - Consider using masks for smoother blending or more complex shapes.
- Use `cv2` functions for filters now (e.g., `cv2.GaussianBlur`, `cv2.resize` for pixelation). These are already C++-optimized under the hood.

#### 2. Python Parallelism
- **Data Pre-processing/Post-processing:** If any parts of your pipeline (e.g., converting frame formats, drawing overlays) are CPU-bound and independent, try using multiprocessing or threading (e.g., for background tasks or handling UI updates separately).
- **Filter Application (if multiple ROIs/filters):** If you detect multiple hands/fingers, or want to apply multiple filters, explore applying these operations in parallel for different ROIs or filter stages.

#### 3. Performance Benchmarking (Iteration 1)
- Measure the FPS of the entire pipeline (capture → hand detection → gesture → ROI processing → display).
- Quantify the performance of `cv2` filters applied to the ROI. This is your new baseline for Halide/C++.
- Analyze where the bottlenecks are (profiling: e.g., MediaPipe processing, filter application, drawing).

**Output of Phase 3:**
Real-time interactive filter application where filters are applied only to the ROI, with initial Python-level optimizations and documented FPS.

---

### Phase 4: High-Performance Custom Filter with Halide & C++ (pybind11)

**Goal:** Identify a specific, complex, or custom filter bottleneck and re-implement it using Halide via C++ to achieve significant performance gains. This is your core differentiator.

#### 1. Identify a Target Filter for Halide
- Based on your Phase 3 benchmarking, pick one filter that is computationally intensive or offers a unique optimization challenge.
    - **Example:** Your custom pixelation (if `cv2.resize` isn't fast enough for very large ROIs), a custom sharpening filter, or a complex artistic effect you design.

#### 2. Halide C++ Implementation
- Set up a C++ project that can compile Halide code. This typically involves CMake.
- Define your chosen filter algorithm using Halide's C++ API (`Halide::Func`).
- Crucially, write one or more Halide schedules to optimize this filter for your target hardware (CPU, or GPU if you have one). This is where your parallel computing knowledge comes in: tiling, unrolling, vectorization, parallel loops, etc.
- Test this C++ Halide implementation independently to verify correctness and initial performance.

#### 3. pybind11 for Python Bindings
- Modify your C++ project to include `pybind11`.
- Write the `pybind11` wrapper code to expose your Halide-optimized C++ filter function to Python.
- Compile your C++ project to create a Python extension module (e.g., `_my_custom_filters.so` or `.pyd`).

#### 4. Integrate into Python Application
- In your main Python script, import your newly created C++ module.
- Replace the Python/OpenCV implementation of your chosen filter with a call to your Halide-optimized C++ function when that filter is activated.

#### 5. Rigorous Benchmarking (Iteration 2)
- **Quantify the Speedup:** Perform detailed benchmarks showing the FPS of the entire pipeline with and without the Halide-optimized filter.
- Compare the performance of the Halide version against the pure Python/NumPy version and the `cv2` version for that specific filter.
- Document the specific Halide schedules you used and why they resulted in performance improvements (e.g., "By fusing stages and vectorizing over X, inference time for the pixelation filter reduced from Y ms to Z ms").

**Output of Phase 4:**
A fully functional real-time interactive filter app with at least one filter demonstrably accelerated by your custom Halide/C++ implementation. This is the core of your unique portfolio piece.

---

### Phase 5: Refinement, UI, and Portfolio Documentation

**Goal:** Polish the application, enhance user interaction, and create a compelling portfolio.

#### 1. User Interface (Optional, but Recommended)
- Implement a simple GUI using `tkinter`, `PyQt`, or Dear ImGui (if you want to delve into C++ UI binding for performance-critical UIs, though Python UIs are fine).
- Allow users to select filters, adjust filter parameters (e.g., blur radius, pixelation block size), change ROI size, or switch gesture mappings.

#### 2. Refine Gestures
- Make your gesture recognition more robust. Handle false positives/negatives.

#### 3. Error Handling & Robustness
- Add basic error handling (e.g., if webcam fails).

#### 4. Code Clean-up & Comments
- Ensure your code is well-structured, modular, and clearly commented.

#### 5. Comprehensive README.md (Crucial for Portfolio)
- **Project Overview:** What does it do? Why is it unique/interesting?
- **Technical Stack:** List all technologies used (Python, OpenCV, MediaPipe, C++, Halide, pybind11, NumPy, etc.).
- **Features:** List all filters, gestures, UI elements.
- **Installation/Usage:** Clear instructions on how to set up and run the project.
- **Key Contributions / Your Skills:** This is where you shine. Explicitly state how you applied your parallel computing and optimization skills. Detail the benchmarks and quantifiable performance improvements you achieved with Halide/C++ and other techniques. Include graphs/tables.
- **Challenges & Solutions:** Discuss problems you encountered and how you solved them.
- **Future Work:** Ideas for further development.
- **Demo Video:** Create a high-quality, short (1-3 minute) video demonstrating the application in action. Highlight the real-time performance and showcase the Halide-accelerated filter clearly.

**Output of Phase 5:**
A polished, well-documented, high-performance interactive video filter application ready for your GitHub portfolio, accompanied by a compelling README and demo video.

---

## Key Principles Throughout

- **Iterate and Benchmark:** Don't build everything at once. Build a small piece, measure its performance, then optimize.
- **Version Control:** Use Git from day one. Commit frequently.
- **Keep it Simple (Initially):** Don't try to optimize everything at once. Focus on the most impactful bottlenecks.
- **Document Your Progress:** Keep notes on your design choices, challenges, and performance findings.