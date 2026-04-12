def process_message():
  pass

def poll(wait_time=20):
  pass

if __name__ == "__main__":
  from .. import create_app
  app = create_app()

  with app.app_context():
    poll(wait_time=20)