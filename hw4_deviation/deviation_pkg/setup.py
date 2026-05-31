from setuptools import find_packages, setup

package_name = 'deviation_pkg'

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
    maintainer='Vyacheslav Mizharev',
    maintainer_email='mizharev@example.com',
    description='Action server and client for computing deviations from the mean',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'server = deviation_pkg.server:main',
            'client = deviation_pkg.client:main',
        ],
    },
)
