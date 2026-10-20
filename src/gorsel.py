"""Ortak grafik stili. Raporda tüm grafikler aynı görünsün diye herkes bunu kullanır."""
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import AYAR, GRAFIK_KLASOR, PROJEKSIYON_BASLANGIC


def stil_ayarla() -> None:
    sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")
    plt.rcParams.update({"figure.figsize": (10, 5.5), "axes.titleweight": "bold",
                         "axes.spines.top": False, "axes.spines.right": False})


def projeksiyon_isaretle(ax, etiket: bool = True) -> None:
    """Projeksiyon yıllarını gölgeler. Zaman serisi grafiklerinde HER ZAMAN kullanın."""
    sag = ax.get_xlim()[1]
    if sag <= PROJEKSIYON_BASLANGIC:
        return
    ax.axvspan(PROJEKSIYON_BASLANGIC, sag, color="grey", alpha=0.08, zorder=0)
    ax.axvline(PROJEKSIYON_BASLANGIC, ls="--", lw=1, color="grey")
    if etiket:
        ax.text(PROJEKSIYON_BASLANGIC, ax.get_ylim()[1], "  BM projeksiyonu →",
                va="top", fontsize=9, color="dimgrey")
    ax.set_xlim(right=sag)


def kaynak_notu(fig, ek: str = "") -> None:
    fig.text(0.01, -0.02, "Kaynak: BM Dünya Nüfus Beklentileri 2024 (WPP2024)" + (f" · {ek}" if ek else ""),
             fontsize=8, color="dimgrey", ha="left")


def kaydet(fig, ad: str) -> None:
    """ad modül adıyla başlamalı: 'yas_yapisi_bolge_medyan_yas'"""
    GRAFIK_KLASOR.mkdir(parents=True, exist_ok=True)
    yol = GRAFIK_KLASOR / f"{ad}.png"
    fig.savefig(yol, dpi=AYAR["grafik"]["dpi"], bbox_inches="tight")
    plt.close(fig)
    print(f"Grafik: reports/figures/{yol.name}")
