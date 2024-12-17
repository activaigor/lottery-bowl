import argparse
import grpc
import lottery_bowl_pb2
import lottery_bowl_pb2_grpc


arg_parser = argparse.ArgumentParser(description='Lottery Bowl Client')
arg_parser.add_argument('--refill', type=int, help='Refill the bowl with a specified number of lots')
arg_parser.add_argument('--grab', action='store_true', help='Grab a lot from the bowl')
arg_parser.add_argument('--size', action='store_true', help='Get a size of the bowl')

args = arg_parser.parse_args()

channel = grpc.insecure_channel('localhost:50051')
stub = lottery_bowl_pb2_grpc.BowlServiceStub(channel)

if args.refill:
    refill_response = stub.RefillBowl(lottery_bowl_pb2.RefillBowlRequest(amount=args.refill))
    print(refill_response.message)
elif args.grab:
    grab_lot_response = stub.GrabLot(lottery_bowl_pb2.GrabLotRequest())
    if not grab_lot_response.value:
        print("Bowl is empty")
    else:
        print(f"Grabbed lot: {grab_lot_response.value}")
elif args.size:
    size = stub.GetSize(lottery_bowl_pb2.GetSizeRequest())
    print(size.result)
else:
    print("No command specified")