import argparse, os
from jinja2 import Environment, PackageLoader, select_autoescape
from parse_xdf import XdfParser, XdfElementType

def main(args: object) -> None:
	if not os.path.isfile(args.filename):
		print(f'[!] Input filename doesn\'t exist: {args.filename}')
		return

	env = Environment(
		loader=PackageLoader('xdf2readme'),
		autoescape=select_autoescape()
	)

	xdf = XdfParser(args.filename).parse()

	template = env.get_template(args.template)
	template.globals['XdfElementType'] = XdfElementType

	with open(args.output, 'w+') as output:
		output.write(template.render(xdf=xdf))

	print('[*] Saved to {}'.format(os.path.abspath(args.output)))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog='XDL2README',
		description='Generate short markdown summaries from TunerPro XDL definition files'
	)
	parser.add_argument('filename')
	parser.add_argument('-t', '--template', default='templates/opengk_template.md', help='Template to use')
	parser.add_argument('-o', '--output', default='README.md', help='Output filename')
	args = parser.parse_args()
	main(args)

