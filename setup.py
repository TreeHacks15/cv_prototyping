from setuptools import setup, find_packages

setup(
		name='cv_prototyping',
		version='0.1',
		author="Brandon Garcia, Jay Hack, Lucas Hansen and Alec Winograd",
		author_email="(bgarcia7|jhack|lucash|awinograd)@stanford.edu",
		description="CV algorithms for interpreting planar surfaces in 3D",
		packages=find_packages(),
		include_package_data=True,
		install_requires=[
			'numpy',
			'scipy',
			'scikit-learn',
			'scikit-image',
			# 'cv2',
			'PIL'
		]
)

