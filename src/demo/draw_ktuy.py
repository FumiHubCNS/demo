"""
draw_ktuy.py
============

KTUY質量公式を使って計算した核図表と液滴モデルとの質量欠損差を描画するコード
"""
import pathlib
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

this_file_path = pathlib.Path(__file__).parent
src_path = pathlib.Path(__file__).parent.parent

def main() -> None:
    """
    メイン関数
    """

    base_inputpath = src_path / 'input'

    ktuy = pd.read_csv(base_inputpath / 'ktuy05_exist.csv')
    ame20 = pd.read_csv(base_inputpath / 'ame2020_wb.csv')
    ktuy_magic = pd.read_csv(base_inputpath / 'magic_number_ktuy05.csv')
    sabilities = pd.read_csv(base_inputpath / 'stable_nuclei.csv')

    # 質量欠損差を計算
    ame20['diff'] = (ame20.M_ex - ame20.M_wb) / 1.e3
    n_vals = np.sort(ame20['N'].unique())
    z_vals = np.sort(ame20['Z'].unique())
    n_edges = np.r_[n_vals - 0.5, n_vals[-1] + 0.5]
    z_edges = np.r_[z_vals - 0.5, z_vals[-1] + 0.5]

    # KTUY質量公式において存在できる原子核を抜き出す
    exist = ktuy[ktuy['exist'] == True]

    ms = 2

    grid = (
        ame20
        .pivot(index='Z', columns='N', values='diff')
        .reindex(index=z_vals, columns=n_vals)
        .to_numpy()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.viridis

    X, Y = np.meshgrid(n_edges, z_edges)

    ax.scatter(exist["N"], exist["Z"], s=ms, c='gray', marker=',', label='KTUY05')

    for i in range(len(ktuy_magic)):

        if not (np.isnan(ktuy_magic.N[i])) and (ktuy_magic.N[i] < exist.N.max()):
            valmagic = [float(ktuy_magic.N[i]), float(ktuy_magic.N[i])]
            ax.plot(valmagic, [0, exist.Z.max()], color="gray", zorder=-1, lw=0.75, ls='-.')

        if not (np.isnan(ktuy_magic.Z[i])) and (ktuy_magic.Z[i] < exist.Z.max()):
            valmagic = [float(ktuy_magic.Z[i]), float(ktuy_magic.Z[i])]
            ax.plot([0, exist.N.max()], valmagic, color="gray", zorder=-1, lw=0.75, ls='-.')

    c = ax.pcolormesh(X, Y, grid, cmap=cmap, shading='flat')

    ax.scatter(sabilities["N"], sabilities["Z"], s=ms, c='black', marker=',', label='Stable')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(c, cax=cax)
    cbar.set_label(r'Mass Difference between AME2020 and Bethe-Weizsäcker [MeV]')

    ax.set_xlabel('Neutron Number (N)')
    ax.set_ylabel('Proton Number (Z)')

    ax.set_xlim(0, exist.N.max())
    ax.set_ylim(0, exist.Z.max())
    ax.legend(loc='upper left')

    ax.set_aspect("equal")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()