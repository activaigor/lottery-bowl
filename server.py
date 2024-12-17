from typing import Optional
import grpc
import concurrent.futures
import time
import queue
import random

import lottery_bowl_pb2
import lottery_bowl_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BowlService(lottery_bowl_pb2_grpc.BowlServiceServicer):
    bowl = queue.Queue()

    def GetSize(self, request, context):
        return lottery_bowl_pb2.GetSizeResponse(result=self.bowl.qsize())

    def GrabLot(self, request, context):
        lot = lottery_bowl_pb2.Lot(value=self._get_from_bowl())
        return lot

    def RefillBowl(self, request, context):
        self.bowl.queue.clear()

        options = ["no"] * (request.amount - 1) + ["yes"]
        random.shuffle(options)
        for o in options:
            self.bowl.put(o)

        return lottery_bowl_pb2.RefillBowlResponse(message=f"Successfully added {request.amount} lots to the bowl")
    
    def _get_from_bowl(self) -> Optional[str]:
        try:
            return self.bowl.get_nowait()
        except queue.Empty:
            return None


def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    lottery_bowl_pb2_grpc.add_BowlServiceServicer_to_server(BowlService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
