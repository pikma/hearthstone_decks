import pickle

def cache_result_in(file_name):
  def wrap(f):
    def wrapped():
      try:
        with open(file_name, 'rb') as read_file:
          result = pickle.load(read_file)
          return result
      except:
        result = f()
        with open(file_name, 'wb') as write_file:
          pickle.dump(result, write_file)
        return result
    return wrapped
  return wrap
