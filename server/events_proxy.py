import zmq


def main():
    try:
        context = zmq.Context()
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:5549")
        frontend.setsockopt(zmq.SUBSCRIBE, b'')

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:5550")

        zmq.proxy(frontend, backend)
    except Exception as e:
        print(e)
        print("bringing down zmq device")
    finally:
        frontend.close()
        backend.close()
        context.term()


if __name__ == '__main__':
    main()
