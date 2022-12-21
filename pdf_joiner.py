import argparse
import os
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--Output', help = 'Define o arquivo de saída')
parser.add_argument('-bm', '--Bookmarks',action='store_true', help = 'Cria um novo arquivo pdf com marcadores')

args = parser.parse_args()

if args.Output:
	output = args.Output
else:
	output = 'joined_files.pdf'

pdf_list = os.listdir()

merger = PdfFileMerger()

bookmarks = list()

for pdf_file in pdf_list:
	ext = os.path.splitext(pdf_file)[1]

	if ext.lower() != '.pdf':
		continue
	print(pdf_file)
	reader = PdfFileReader(pdf_file)
	bookmarks.append((os.path.splitext(pdf_file)[0], reader.numPages))
	
	merger.append(pdf_file)

merger.write(output)
merger.close()

if args.Bookmarks:
	reader = PdfFileReader(output)
	writer = PdfFileWriter()
	writer.appendPagesFromReader(reader)
	counter = 0
	writer.addBookmark(bookmarks[0][0], 0, parent=None)
	counter += bookmarks[0][1]


	for bookmark in bookmarks[1:]:
		writer.addBookmark(bookmark[0], counter, parent=None)
		counter += bookmark[1]

	with open(output + '_tmp', 'wb') as f:
		writer.write(f)

	os.remove(output)
	os.rename(output + '_tmp', output)
