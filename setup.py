from setuptools import setup, find_packages

setup(
    name="RealTimeCVHalide",
    version="0.1.0",
    description="Real-time interactive video filter application with Python, OpenCV, and Halide integration",
    author="Yusuf Butt",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        # Add other dependencies as needed
    ],
    include_package_data=True,
    python_requires=">=3.7",
)
