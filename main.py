import numpy as np
import tkinter as tk


def calculate_impedance():
    try:
        w = float(width_entry.get()) / 1000
        t = float(height_entry.get()) / 1000
        h = float(isolation_entry.get()) / 1000
        er = float(er_entry.get())

        print(f"track_width = {w}, track_height = {t}, isolation_height = {h}, er = {er}")

        w_eff = w + (1.25 * t / np.pi) * (1 + np.log(4 * np.pi * w / t))

        u = w_eff / h
        a = 1 + (1 / 49) * np.log((u ** 4 + (u / 52) ** 2) / (u ** 4 + 0.432)) + (1 / 18.7) * np.log(
            1 + (u / 18.1) ** 3)
        b = 0.564 * ((er - 0.9) / (er + 3)) ** 0.053
        e_eff = ((er + 1) / 2) + ((er - 1) / 2) * (1 + 10 / u) ** (-a * b)

        print(f"Effective width = {w_eff}, Effective dielectric constant = {e_eff}")

        if u <= 1:
            z0 = (60 / np.sqrt(e_eff)) * np.log(8 / u + 0.25 * u)
        else:
            z0 = (120 * np.pi) / (np.sqrt(e_eff) * (u + 1.393 + 0.667 * np.log(u + 1.444)))

        print(f"z0 = {z0}")
        result_label.config(text=f"Impedance: {z0:.2f} Ω")
    except ValueError:
        result_label.config(text="Error: Enter numerical values")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        result_label.config(text=f"Error: {str(e)}")


root = tk.Tk()
root.title("PCB Trace Impedance Calculator")

tk.Label(root, text="Trace Width (mm):").grid(row=0, column=0)
width_entry = tk.Entry(root)
width_entry.grid(row=0, column=1)

tk.Label(root, text="Trace Height (mm):").grid(row=1, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

tk.Label(root, text="Isolation Height (mm):").grid(row=2, column=0)
isolation_entry = tk.Entry(root)
isolation_entry.grid(row=2, column=1)

tk.Label(root, text="Dielectric Constant:").grid(row=3, column=0)
er_entry = tk.Entry(root)
er_entry.grid(row=3, column=1)

calc_button = tk.Button(root, text="Calculate Impedance", command=calculate_impedance)
calc_button.grid(row=4, columnspan=2)

result_label = tk.Label(root, text="Impedance: ")
result_label.grid(row=5, columnspan=2)

root.mainloop()
