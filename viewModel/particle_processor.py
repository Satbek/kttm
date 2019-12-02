from PyQt5 import QtCore

class ParticleProcessor(QtCore.QThread):
    send_particles_signal = QtCore.pyqtSignal(list)
    def __init__(self, solver, time_interval, q_in):
        """
        solver - model_solver
        q_in - queue to get particles
        time_interval - time interval for solver
        """
        super().__init__()
        self.solver = solver
        self.time_interval = time_interval
        self.q_in = q_in

    def run(self):
        curr_particles = self.q_in.get()
        while True:
            if len(curr_particles) > 0:
                result = self.solver.solve(curr_particles, self.time_interval)
                self.send_particles_signal.emit(result)
            curr_particles = self.q_in.get()