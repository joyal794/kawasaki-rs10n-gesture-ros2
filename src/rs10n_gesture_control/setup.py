from setuptools import find_packages, setup

package_name = 'rs10n_gesture_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='joyal05',
    maintainer_email='joyal05@example.com',
    description='Gesture control and joint motion simulation for RS10N robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_motion = rs10n_gesture_control.joint_motion_node:main',
            'gesture_detector = rs10n_gesture_control.gesture_detector_node:main',
        ],
    },
)
