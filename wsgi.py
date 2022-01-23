from distutils.log import debug

import dailyUpdates

handler = dailyUpdates.create_app()

if __name__ == "__main__":
    print("Running in debug mode.")
    handler.run(host="0.0.0.0", debug=True)
