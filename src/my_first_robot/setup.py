from setuptools import find_packages, setup

package_name = 'my_first_robot'

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
    maintainer='lyj3594513',
    maintainer_email='lyj3594513@naver.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'hello_node = my_first_robot.hello_node:main',
        'publisher_node = my_first_robot.publisher_node:main',
        'subscriber_node = my_first_robot.subscriber_node:main',
        'velocity_publisher = my_first_robot.velocity_publisher:main',
        'motion_sequence = my_first_robot.motion_sequence:main',
        'go_to_goal = my_first_robot.go_to_goal:main',
        'waypoint_controller = my_first_robot.waypoint_controller:main',
    ],
},
)