import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple("Event", "time proc action")


# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):  # <1>
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, "leave garage")  # <2>
    for i in range(trips):  # <3>
        time = yield Event(time, ident, "pick up passenger")  # <4>
        time = yield Event(time, ident, "drop off passenger")  # <5>

    yield Event(time, ident, "going home")  # <6>
    # end of taxi process # <7>


# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):  # <1>
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
        for _, proc in sorted(self.procs.items()):  # <2>
            first_event = next(proc)  # <3>
            self.events.put(first_event)  # <4>

        # main loop of the simulation
        sim_time = 0  # <5>
        while sim_time < end_time:  # <6>
            if self.events.empty():  # <7>
                print("*** end of events ***")
                break

            current_event = self.events.get()  # <8>
            sim_time, proc_id, previous_action = current_event  # <9>
            print("taxi:", proc_id, proc_id * "   ", current_event)  # <10>
            active_proc = self.procs[proc_id]  # <11>
            next_time = sim_time + compute_duration(previous_action)  # <12>
            try:
                next_event = active_proc.send(next_time)  # <13>
            except StopIteration:
                del self.procs[proc_id]  # <14>
            else:
                self.events.put(next_event)  # <15>
        else:  # <16>
            msg = "*** end of simulation time: {} events pending ***"
            print(msg.format(self.events.qsize()))


# END TAXI_SIMULATOR


def compute_duration(previous_action):
    """Compute action duration using exponential distribution"""
    if previous_action in ["leave garage", "drop off passenger"]:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == "pick up passenger":
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == "going home":
        interval = 1
    else:
        raise ValueError("Unknown previous_action: %s" % previous_action)
    return int(random.expovariate(1 / interval)) + 1


def main(
    end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None
):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {
        i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERVAL)
        for i in range(num_taxis)
    }
    sim = Simulator(taxis)
    sim.run(end_time)


main()
