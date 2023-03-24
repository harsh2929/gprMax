import numpy as np
from gprMax.constants import c, e0
from gprMax.waveforms import Waveform


def hertzian_dipole_fs(iterations: int, dt: float, dxdydz: tuple, rx: tuple) -> np.ndarray:
    """Analytical solution of a z-directed Hertzian dipole in free space with a Gaussian current waveform (http://dx.doi.org/10.1016/0021-9991(83)90103-1).

    Args:
        iterations (int): Number of time steps.
        dt (float): Time step (seconds).
        dxdydz (tuple[float, float, float]): Spatial resolution (metres) as a tuple of floats.
        rx (tuple[float, float, float]): Coordinates of receiver position relative to transmitter position (metres) as a tuple of floats.

    Returns:
        fields (np.ndarray): Array containing electric and magnetic field components.
    """

    # Create waveform objects for the different types of waveforms
    w = Waveform(type='gaussianprime', amp=1, freq=1e9)
    wint = Waveform(type='gaussian', amp=w.amp, freq=w.freq)
    wdot = Waveform(type='gaussiandoubleprime', amp=w.amp, freq=w.freq)

    # Create an array to store the electric and magnetic field components at each time step
    fields = np.zeros((iterations, 6))

    # Unpack the spatial resolution tuple
    dx, dy, dz = dxdydz

    # Length of Hertzian dipole
    dl = dz

    # Unpack the receiver position tuple
    x, y, z = rx
    sign_z = 1 if z == 0 else np.sign(z)  # Check if z == 0 and set the sign of z accordingly

    # Calculate the coordinates and the time delay for each of the FDTD components

    # Ex component
    Ex_x, Ex_y, Ex_z = x + 0.5 * dx, y, z - 0.5 * dz
    Er_x = np.sqrt(Ex_x ** 2 + Ex_y ** 2 + Ex_z ** 2)
    tau_Ex = Er_x / c

    # Ey component
    Ey_x, Ey_y, Ey_z = x, y + 0.5 * dy, z - 0.5 * dz
    Er_y = np.sqrt(Ey_x ** 2 + Ey_y ** 2 + Ey_z ** 2)
    tau_Ey = Er_y / c

    # Ez component
    Ez_x, Ez_y, Ez_z = x, y, z
    Er_z = np.sqrt(Ez_x ** 2 + Ez_y ** 2 + Ez_z ** 2)
    tau_Ez = Er_z / c

    # Hx component
    Hx_x, Hx_y, Hx_z = x, y + 0.5 * dy, z
    Hr_x = np.sqrt(Hx_x ** 2 + Hx_y ** 2 + Hx_z ** 2)
    tau_Hx = Hr_x / c

    # Hy component
    Hy_x, Hy_y, Hy_z = x + 0.5 * dx, y, z
    Hr_y = np.sqrt(Hy_x ** 2 + Hy_y ** 2 + Hy_z ** 2)
    tau_Hy = Hr_y / c
    
    # Coordinates of Rx for Hz FDTD component
    Hz_x = x + 0.5 * dx
    Hz_y = y + 0.5 * dy
    Hz_z = z - 0.5 * dz
    Hr_z = np.sqrt((Hz_x**2 + Hz_y**2 + Hz_z**2))
    tau_Hz = Hr_z / c

    # Initialise fields
    fields = np.zeros((iterations, 6))

    # Calculate fields
    for timestep in range(iterations):

        # Calculate values for waveform, I * dl (current multiplied by dipole length) to match gprMax behaviour
        fint_Ex = wint.calculate_value((timestep * dt) - tau_Ex, dt) * dl
        f_Ex = w.calculate_value((timestep * dt) - tau_Ex, dt) * dl
        fdot_Ex = wdot.calculate_value((timestep * dt) - tau_Ex, dt) * dl

        fint_Ey = wint.calculate_value((timestep * dt) - tau_Ey, dt) * dl
        f_Ey = w.calculate_value((timestep * dt) - tau_Ey, dt) * dl
        fdot_Ey = wdot.calculate_value((timestep * dt) - tau_Ey, dt) * dl

        fint_Ez = wint.calculate_value((timestep * dt) - tau_Ez, dt) * dl
        f_Ez = w.calculate_value((timestep * dt) - tau_Ez, dt) * dl
        fdot_Ez = wdot.calculate_value((timestep * dt) - tau_Ez, dt) * dl

        fint_Hx = wint.calculate_value((timestep * dt) - tau_Hx, dt) * dl
        f_Hx = w.calculate_value((timestep * dt) - tau_Hx, dt) * dl
        fdot_Hx = wdot.calculate_value((timestep * dt) - tau_Hx, dt) * dl

        fint_Hy = wint.calculate_value((timestep * dt) - tau_Hy, dt) * dl
        f_Hy = w.calculate_value((timestep * dt) - tau_Hy, dt) * dl
        fdot_Hy = wdot.calculate_value((timestep * dt) - tau_Hy, dt) * dl

        fint_Hz = wint.calculate_value((timestep * dt) - tau_Hz, dt) * dl
        f_Hz = w.calculate_value((timestep * dt) - tau_Hz, dt) * dl
        fdot_Hz = wdot.calculate_value((timestep * dt) - tau_Hz, dt) * dl

        # Ex
        fields[timestep, 0] = ((Ex_x * Ex_z) / (4 * np.pi * e0 * Er_x**5)) * (3 * (fint_Ex + (tau_Ex * f_Ex)) + (tau_Ex**2 * fdot_Ex))

        # Ey 
        try:
            tmp = Ey_y / Ey_x
        except ZeroDivisionError:
            tmp = 0
        fields[timestep, 1] = tmp * ((Ey_x * Ey_z) / (4 * np.pi * e0 * Er_y**5)) * (3 * (fint_Ey + (tau_Ey * f_Ey)) + (tau_Ey**2 * fdot_Ey))

        # Ez
        fields[timestep, 2] = (1 / (4 * np.pi * e0 * Er_z**5)) * ((2 * Ez_z**2 - (Ez_x**2 + Ez_y**2)) * (fint_Ez + (tau_Ez * f_Ez)) - (Ez_x**2 + Ez_y**2) * tau_Ez**2 * fdot_Ez)

        # Hx
        fields[timestep, 3] = - (Hx_y / (4 * np.pi * Hr_x**3)) * (f_Hx + (tau_Hx * fdot_Hx))

        # Hy
        try:
            tmp = Hy_x / Hy_y
        except ZeroDivisionError:
            tmp = 0
        fields[timestep, 4] = - tmp * (- (Hy_y / (4 * np.pi * Hr_y**3)) * (f_Hy + (tau_Hy * fdot_Hy)))

        # Hz
        fields[timestep, 5] = 0

    return fields
