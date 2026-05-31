from setuptools import find_packages, setup

package_name = 'random_sort'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='example',
    maintainer_email='example.com',
    description='Publishes random natural numbers; second node accumulates and sorts them',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'number_publisher = random_sort.number_publisher:main',
            'sorter_node = random_sort.sorter_node:main',
        ],
    },
)
