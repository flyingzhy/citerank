import csv
import os

import six

TEMP_FILE_SUFFIX = '.part'

def iter_read_csv_columns(filename, columns):
  with open(filename, 'r') as csv_f:
    csv_reader = csv.reader(csv_f)
    first_row = True
    indices = None
    for row in csv_reader:
      if first_row:
        indices = [row.index(c) for c in columns]
        first_row = False
      else:
        yield [row[i] for i in indices]

def gzip_open(filename, mode):
  import gzip

  if mode == 'w' and not six.PY2:
    from io import TextIOWrapper

    return TextIOWrapper(gzip.open(filename, mode))
  else:
    return gzip.open(filename, mode)

def optionally_compressed_open(filename, mode):
  if filename.endswith('.gz') or filename.endswith('.gz' + TEMP_FILE_SUFFIX):
    return gzip_open(filename, mode)
  else:
    return open(filename, mode)

def open_csv_output(filename):
  return optionally_compressed_open(filename, 'w')

def write_csv_rows(writer, iterable):
  if six.PY2:
    for row in iterable:
      writer.writerow([
        x.encode('utf-8') if isinstance(x, six.text_type) else x
        for x in row
      ])
  else:
    for row in iterable:
      writer.writerow(row)

def write_csv_row(writer, row):
  write_csv_rows(writer, [row])

def write_csv(filename, columns, iterable):
  temp_filename = filename + TEMP_FILE_SUFFIX
  if os.path.isfile(filename):
    os.remove(filename)
  with open_csv_output(temp_filename) as csv_f:
    writer = csv.writer(csv_f)
    write_csv_rows(writer, [columns])
    write_csv_rows(writer, iterable)
  os.rename(temp_filename, filename)
