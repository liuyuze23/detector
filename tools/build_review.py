from pathlib import Path
from textwrap import dedent

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "review"
PDF_OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF_OUT.mkdir(parents=True, exist_ok=True)


def writable_pdf_path():
    candidates = [
        PDF_OUT / "temperature_detector_review.pdf",
        PDF_OUT / "temperature_detector_review_with_figures.pdf",
        PDF_OUT / "temperature_detector_review_with_figures_v2.pdf",
    ]
    for candidate in candidates:
        try:
            with candidate.open("ab"):
                pass
            return candidate
        except PermissionError:
            continue
    return PDF_OUT / "temperature_detector_review_with_figures_latest.pdf"


refs = [
    ("veale2020", "Veale et al. (2020)", "Characterization of the Uniformity of High-Flux CdZnTe Material", "Sensors 20, 2747", "CdZnTe", "Redlen/STFC HEXITEC; 28 C and 18 C stability comparison."),
    ("cline2024", "Cline et al. (2024)", "Characterisation of Redlen HF-CdZnTe at >10^6 ph s^-1 mm^-2 using HEXITEC MHz", "Journal of Synchrotron Radiation", "CdZnTe", "HEXITEC MHz, 20 C ASIC temperature, high-flux leakage/baseline drift."),
    ("montemont2013", "Montemont et al. (2013)", "An Autonomous CZT Module for X-ray Diffraction Imaging", "IEEE NSS/MIC", "CdZnTe", "CEA-Leti/Morpho autonomous XDi module, 25 C module setting."),
    ("kosciesza2013", "Kosciesza et al. (2013)", "X-ray diffraction imaging system for the detection of illicit substances using pixelated CZT-detectors", "IEEE NSS/MIC", "CdZnTe", "Morpho/CEA XDi system, 22 +/- 1 C, 0.1 keV/C peak shift."),
    ("greenberg2014", "Greenberg, Iniewski and Brady (2014)", "CZT Detector Modeling for Coded Aperture X-ray Diffraction Imaging Applications", "IEEE NSS/MIC", "CdZnTe", "Duke/Redlen detector model for CAXI energy resolution and count-rate tradeoffs."),
    ("greenberg2016", "Greenberg et al. (2016)", "High precision, medium flux rate CZT spectroscopy for coherent scatter imaging", "SPIE ADIX 9847", "CdZnTe", "Duke/Redlen medium-flux CZT coherent scatter detector."),
    ("stryker2021", "Stryker et al. (2021)", "X-ray fan beam coded aperture transmission and diffraction imaging for fast material analysis", "Scientific Reports 11, 10585", "Not CdZnTe/CdTe", "Duke/Quadridox system prototype using energy-integrating flat panel; application benchmark."),
    ("minami2023", "Minami et al. (2023)", "2-mm-thick large-area CdTe double-sided strip detectors for high-resolution spectroscopic imaging", "arXiv/NIM A related", "CdTe", "2 mm CdTe DSD operated at -20 C and 500 V."),
    ("franklin2024", "Franklin et al. (2024)", "Characterizing electron-collecting CdTe for use in a 77 ns burst-rate imager", "Journal of Synchrotron Radiation 31", "CdTe", "Acrorad electron-collecting CdTe, vacuum + TEC +/-0.1 C, polarization vs temperature/bias."),
    ("greiffenberg2025", "Greiffenberg et al. (2025)", "Signal stability of high-Z sensors at synchrotron light sources", "JINST 20, P01031", "CdTe; CdZnTe; GaAs:Cr", "Direct 0/15/30 C comparison of Acrorad CdTe and Redlen CdZnTe under high flux."),
    ("thomas2017", "Thomas et al. (2017)", "Characterisation of Redlen high-flux CdZnTe", "JINST 12, C12045", "CdZnTe", "Redlen high-flux CdZnTe transport, 303 +/- 1 K, RH <10%."),
    ("prokesch2016", "Prokesch et al. (2016)", "CdZnTe Detectors Operating at X-ray Fluxes of 100 Million Photons/(mm2 sec)", "IEEE TNS 63", "CdZnTe", "eV Products THM CdZnTe at 23-28 C and 1e8 ph/mm2/s."),
    ("baussens2022", "Baussens et al. (2022)", "Characterization of High-Flux CdZnTe with optimized electrodes for 4th generation synchrotrons", "JINST 17, C11008", "CdZnTe", "Redlen HF-CZT, optimized Au/Pt/Pt contacts, 20 C, water cooling + nitrogen."),
    ("bettelli2023", "Bettelli et al. (2023)", "High performance platinum contacts on high-flux CdZnTe detectors", "Scientific Reports 13, 17963", "CdZnTe", "Platinum contacts and CdTeO3 interfacial layer on Redlen HF-CZT."),
    ("astromskas2016", "Astromskas et al. (2016)", "Evaluation of Polarization Effects of e-Collection Schottky CdTe Medipix3RX Hybrid Pixel Detector", "IEEE TNS 63", "CdTe", "Acrorad Schottky CdTe/Medipix3RX, temperature, flux and bias-reset polarization study."),
    ("becker2017", "Becker et al. (2017)", "Sub-Microsecond X-Ray Imaging Using Hole-Collecting Schottky type CdTe with Charge-Integrating Pixel Array Detectors", "JINST", "CdTe", "Acrorad CdTe PAD, 0 C operation, persistence from -30 to +20 C."),
    ("cola2009", "Cola and Farella (2009)", "The polarization mechanism in CdTe Schottky detectors", "Applied Physics Letters 94, 102113", "CdTe", "Pockels-effect electric-field measurement and 0.62 eV activation energy."),
    ("meyer2022", "Meyer et al. (2022)", "Observation of radiation damage in CdTe Schottky sensors created by 20 keV photons", "JINST 17, P06035", "CdTe", "Acrorad CdTe/JUNGFRAU, 0-30 C, water cooling + nitrogen, radiation history."),
    ("toyama2006", "Toyama et al. (2006)", "Quantitative Analysis of Polarization Phenomena in CdTe Radiation Detectors", "Japanese Journal of Applied Physics 45, 8842", "CdTe", "Acrorad Al/CdTe/Pt, 0-50 C, deep-acceptor model."),
    ("principato2012", "Principato et al. (2012)", "Time-dependent current-voltage characteristics of Al/p-CdTe/Pt x-ray detectors", "Journal of Applied Physics 112, 094506", "CdTe", "Acrorad CdTe, Peltier +/-0.1 C, nitrogen, millisecond-to-1000 s I-V dependence."),
    ("bale2008", "Bale and Szeles (2008)", "Nature of polarization in wide-bandgap semiconductor detectors under high-flux irradiation", "Physical Review B 77, 035205", "CdZnTe", "Core PRB model for high-flux CdZnTe polarization and critical flux."),
]


sections = [
    (
        "引言：从衍射成像需求到温度问题",
        [
            "X 射线衍射成像、energy-dispersive X-ray diffraction (EDXRD)、coherent scatter imaging 和 coded-aperture XRD 都把探测器推到一个尴尬但关键的位置：系统希望在有限采集时间内同时获得空间、能量和散射角信息，而探测器必须在高原子序数吸收效率、能量分辨率、计数率和长期稳定性之间取得平衡。传统高纯锗探测器可以给出优异的能量分辨率，但深冷、真空和维护成本与安检、工业无损检测或便携式谱成像系统并不相容。CdZnTe 和 CdTe 因为高 Z、宽禁带和可近室温运行，被持续推向这些应用场景。",
            "然而，在这些系统中，温度并不是一个简单的环境参数。它通过热激发漏电流、前端电子学噪声、阈值和基线漂移、陷阱俘获/退俘获、空间电荷、极化、afterglow 和偏压稳定性影响最终的谱峰位置、能量分辨率和计数率上限。更重要的是，温度作用的强弱在 CdZnTe 和 CdTe 之间并不相同。Redlen/eV Products 路线的 high-flux CdZnTe 文献反复强调空穴输运和接触工程，使器件可在 20-30 C 左右轻度控温或室温条件下承受高通量；Acrorad CdTe Schottky 文献则显示偏压后极化时间常数对温度极敏感，0 C 和 30 C 的稳定时间可以从数小时缩短到几十分钟。",
            "本综述围绕已经精读的 21 篇本地文献展开，其中 20 篇直接讨论 CdZnTe/CdTe 探测器或其机理，一篇 Duke fan-beam coded-aperture 样机使用能量积分平板而非 CdZnTe/CdTe，本文将其作为应用系统参照而非材料证据。叙述顺序仿照物理类论文 introduction 的推进方式：先提出高 Z 能量分辨探测器在 XRD/EDXRD 中的需求，再讨论温度影响的物理通道，随后分别分析 CdZnTe 和 CdTe 的材料响应，最后回到 CEA-Leti/Morpho/Smiths、Duke/Redlen、Redlen/Canon、Acrorad、Kromek/eV Products、ESRF/IMEM-CNR 等机构和公司的温控工程路线。",
        ],
        ["kosciesza2013", "montemont2013", "greenberg2014", "greenberg2016", "stryker2021", "veale2020", "greiffenberg2025"],
    ),
    (
        "叙述结构与证据分层",
        [
            "本文不按文献逐篇罗列，而按证据功能分层。第一层是物理机理文献：Bale 和 Szeles 解释 CdZnTe 高通量下空穴俘获、正空间电荷和 field pinch 如何限制临界通量；Cola、Toyama 和 Principato 解释 CdTe Schottky 中深受主、退俘获、负空间电荷和 I-V 时间依赖如何导致极化。这一层回答“温度为什么会改变探测器状态”。",
            "第二层是材料和器件文献：Veale、Cline、Thomas、Prokesch、Baussens 和 Bettelli 构成 Redlen/eV high-flux CdZnTe 主线，说明室温或轻度控温下的高通量能力、空穴输运和接触工程；Astromskas、Becker、Meyer、Minami 和 Franklin 构成 Acrorad CdTe 对照主线，说明低温、偏压刷新、真空/氮气封装和剂量历史的重要性。这一层回答“温度改变了哪些可测性能”。",
            "第三层是系统和公司路线文献：Montemont 与 Kosciesza 代表 CEA-Leti/Morpho/Smiths 的 XDi/EDXRD 安检路线，Greenberg 与 Stryker 代表 Duke/Redlen/Quadridox coded-aperture XRD 路线，Baussens/Bettelli 代表 ESRF/IMEM-CNR 面向第四代同步辐射的 high-flux contact engineering 路线。这一层回答“为什么工程系统选择某一恒温点，以及代价是什么”。",
        ],
        ["bale2008", "cola2009", "toyama2006", "principato2012", "veale2020", "cline2024", "thomas2017", "prokesch2016", "baussens2022", "bettelli2023", "astromskas2016", "becker2017", "meyer2022", "minami2023", "franklin2024", "montemont2013", "kosciesza2013", "greenberg2014", "greenberg2016", "stryker2021"],
    ),
    (
        "温度影响探测器性能的主要通道",
        [
            "第一条通道是漏电流和电子噪声。温度升高通常增加热激发载流子和接触注入电流，进而提高 shot noise、压缩前端漏电补偿余量，并使阈值和基线校正更困难。Principato 等在 Al/p-CdTe/Pt 探测器中给出一个直观量级：-1000 V 下 pixel current 从 -25 C 的约 2 pA 上升到 40 C 的约 3 nA，差异接近三个数量级。Thomas 等的 Redlen HF-CdZnTe/PIXIE 实验也说明，ASIC 漏电补偿约 250 pA/pixel，漏电不是抽象问题，而会直接限制高增益模式和可测试偏压。",
            "第二条通道是能量分辨率和峰位稳定性。漏电和基线漂移会增加 FWHM；空间电荷和电场重分布会使诱导电荷不足，导致谱峰向低能漂移。CEA-Leti/Morpho XDi 系统给出了工程化的峰位温漂量：像素化 CdZnTe 模块在 20-25 C 范围内 peak shift gradient 约 0.1 keV/C，因此 22 +/- 1 C 的系统恒温足以把峰位漂移控制在约 0.1 keV 量级，小于其约 2.26 keV @59.5 keV 的能量分辨率尺度。CdTe Schottky 则更严重：Toyama 等把 59.5 keV 峰位开始漂移的时间与 depletion width 变窄的时间联系起来，显示峰位漂移是电场结构变化的直接结果。",
            "第三条通道是极化和计数率上限。Bale 和 Szeles 的 PRB 模型为 CdZnTe 高通量极化提供了物理图像：高通量下慢速空穴被快速俘获，正空间电荷在入射侧累积，形成 electric-field pinch point；电子漂移时间变长、寿命降低并复合，谱整体向低能移动，导致阈值以上计数先饱和后下降。模型预测最大可承受通量近似随偏压平方增加，并随温度通过深受主退俘获时间呈指数变化。对 CdTe Schottky，Cola、Toyama、Principato 和 Meyer 等文献共同表明，温度升高会加速深受主退俘获和负空间电荷建立，使偏压诱导极化、漏电上升和响应非均匀性提前发生。",
            "第四条通道是长期稳定性和历史效应。温度控制只能稳定当前工作点，却不能消除所有历史依赖。CdTe 文献中的 bias refresh、forward-bias reset、热退火、辐照损伤和 afterglow 都说明，探测器响应取决于此前偏压、剂量、照射空间分布和等待时间。Becker 等甚至显示某些 persistence 的衰减时间从 +20 C 的约 90 ms 增加到 -30 C 的约 150 ms，说明降温虽然常降低漏电和延缓极化，但并非对所有时间响应指标单调有利。",
        ],
        ["principato2012", "thomas2017", "kosciesza2013", "toyama2006", "bale2008", "cola2009", "meyer2022", "becker2017"],
    ),
    (
        "CdZnTe：近室温稳定、高通量能力与接触工程",
        [
            "CdZnTe 的优势首先体现在室温或轻度控温下的能谱稳定性。CEA-Leti/Morpho 的自主 CZT XDi 模块以 room-temperature CZT 替代 cooled Ge，5 mm 高阻 CdZnTe 与 IDeF-X/ALIGASPECT 读出组合在 25 C 调节条件下达到约 3.8% @60 keV、2.4% @122 keV。后续 XDi 系统把 17 个模块置于长冷却板上，控制在 22 +/- 1 C，40 个模块平均 2.26 +/- 0.13 keV @59.5 keV，并明确给出 0.1 keV/C 的温漂系数。这是一条典型的产品化逻辑：温控不是为了深冷，而是为了使多模块峰位、阈值和标定在安检系统可维护范围内保持一致。",
            "Redlen HF-CdZnTe/HEXITEC 系列进一步把问题推向高通量。Veale 等在 28 C 室温和 18 C 对比条件下测试 Redlen HF-CdZnTe，28 C 下可得到约 0.83 keV @59.54 keV，并显示 24 h 漂移较小；18 C 下 FWHM 漂移更小，但这属于轻度降温而非深冷。Cline 等在 HEXITEC MHz 中使用 20 C ASIC temperature、Peltier、湿控箱和外置除湿模块，证明 >10^6 ph s^-1 mm^-2 条件下仍可做能谱成像，同时暴露局域 excess leakage-current 和基线偏移，说明高通量 CdZnTe 仍需要实时 offset correction 和湿温管理。",
            "高通量 CdZnTe 的材料级核心是空穴输运而不是单纯降温。Thomas 等在 303 +/- 1 K、RH <10% 条件下表征 Redlen high-flux CdZnTe，发现其电子 mu-tau 低于标准光谱级材料，但空穴 mu-tau 约 2.9e-4 cm2/V，较标准 Redlen 提高一个数量级以上。Prokesch 等的 eV Products THM CdZnTe 在 23-28 C、900 V 下承受最高约 1e8 photons/mm2/s 入射通量而无电场极化；对照低通量光谱级 CZT 虽有更好电子 mu-tau，却因空穴 mu-tau 约 5e-6 cm2/V 在 <1 Mcps/mm2 即极化。这说明高通量 XRD/谱成像不能只看低通量能量分辨率，必须看空穴俘获和空间电荷。",
            "接触工程决定 high-flux CdZnTe 能否把高偏压真正用起来。Baussens 等在 Redlen HF-CZT 上使用优化 Au/Pt 和 Pt/Pt 接触，20 C、-1000 V 下暗电流密度约 90 和 60 pA/mm2，并在 20 keV、3e7-8e9 photons/mm2/s 范围内保持 R2 >0.999 的光电流线性；Pt/Pt 样品可测试到 1e12 photons/mm2/s，但 >1e11 photons/mm2/s 出现 hysteresis。Bettelli 等进一步证明 Pt/CdTeO3/CZT 界面阻挡空穴注入并利于抽取，Pt 阳极样品在约 500 V/mm 下约 40 pA/mm2，1200 V/mm 下仍可控制在约 300 pA/mm2。这一组文献说明，对 CdZnTe 而言，最佳工程路线通常是中等温控、低漏电接触、高偏压和高空穴输运协同，而不是把温度越降越低。",
        ],
        ["montemont2013", "kosciesza2013", "veale2020", "cline2024", "thomas2017", "prokesch2016", "bale2008", "baussens2022", "bettelli2023"],
    ),
    (
        "CdTe：低温、偏压刷新与极化历史",
        [
            "CdTe 的高 Z 和成熟晶体工艺使其成为 CdZnTe 的重要对照，但 Schottky CdTe 的温度敏感性更强。Cola 和 Farella 通过 Pockels effect 观察到 CdTe Schottky 电场随时间和温度演化，空间电荷为负，来源于受主缺陷负离化，Arrhenius 激活能为 0.62 +/- 0.02 eV。Toyama 等在 Acrorad Al/CdTe/Pt 中进一步定量化深受主模型：修正模型给出 ET - EV = 0.69 eV，退俘获时间从 0 C 的 4695 min 降至 30 C 的 351 min；20 C、100 V 下阴极侧电场约 61 min 后达到零场，随后 depletion width 缩小并对应 59.5 keV 峰位漂移。",
            "Principato 等把这个问题推进到测量时间尺度本身：Al/p-CdTe/Pt 的 I-V 曲线在 1 ms-1000 s 范围内都存在时间依赖，且即使 <1 s 的延迟也会改变测得电流。Peltier +/-0.1 C 和氮气防凝露是其测量平台的一部分；冷却增加 polarization time，-1000 V 下像素电流在 -25 C 与 40 C 相差接近三数量级。这意味着产品资料或论文中若没有说明 bias 后多久测 I-V，CdTe 漏电数据很难横向比较。",
            "低温 CdTe 可以获得稳定能谱，但工程代价更高。Minami 等的 2 mm 厚 CdTe DSD 在 -20 C、500 V 下实现 2.6 keV @122 keV、4.3 keV @356 keV，并在约 20 h 内能量分辨率变化 <1%。Franklin 等的 electron-collecting Acrorad CdTe 使用真空封装、透明窗口和 TEC +/-0.1 C，在 0 C 和 -200/-400 V 下研究 77 ns burst-rate imager；更高温度和更低偏压会加快极化。Becker 等选择 0 C 作为主要工作点，低温和高电压缩短偏压建立后的稳定时间，但 persistence 释放时间在低温下变长，提示降温不是所有动态指标的单调优化。",
            "CdTe 高通量/连续照射稳定性尤其要谨慎。Astromskas 等在 Acrorad Schottky CdTe/Medipix3RX 中发现，温度、通量和曝光时间共同控制极化速度；高通量下出现 tri-phase pixel 行为，bias reset 可恢复初始响应，但 300 kcps/pixel 条件下需要约 15-20 s off-time 才足以稳定。Meyer 等用 JUNGFRAU 读出比较 Acrorad Schottky 与 ohmic CdTe：0 C、-500 V、低通量下 5 h 几乎无极化，+15 C 约 200 min 出现极化，+30 C 约 35 min 开始极化，约 70 min 后 99% pixels 低于初始平均计数 50%。预辐照区域更抗极化，但以漏电升高为代价；80 C 退火也改变极化过程。这些结果显示，CdTe 系统必须把温度、偏压刷新、剂量历史和接触结构作为一个整体设计。",
        ],
        ["cola2009", "toyama2006", "principato2012", "minami2023", "franklin2024", "becker2017", "astromskas2016", "meyer2022"],
    ),
    (
        "温控工程方案：为什么采用这些温度",
        [
            "从已有系统看，温度设定可以分为三类。第一类是 CdZnTe 安检/EDXRD 模块的室温恒温，例如 CEA-Leti/Morpho XDi 的 22 +/- 1 C 或 25 C。好处是峰位漂移可控、多模块标定一致、无需 HPGe 深冷真空系统；代价是冷却板、温度传感器、系统标定和低于环境运行时的凝露管理。由于散射信号通量低于 CT 高通量场景，这一路线优先保证可维护性和模块化，而不是追求最低噪声。",
            "第二类是 high-flux CdZnTe 的 18-30 C 轻度控温。Redlen/HEXITEC 和 ESRF/IMEM-CNR 文献中常见 Peltier、recirculating chiller、Pt100、湿度控制、氮气或除湿模块。好处是稳定 ASIC、漏电、偏压和基线，同时允许高场工作；代价是功耗、体积、湿度管理、温度梯度和更复杂的机械封装。关键是，这类系统通常不依赖深冷来获得可用性，而是依赖材料空穴输运和接触工程。",
            "第三类是 CdTe Schottky 的低温/TEC/水冷方案，例如 -20 C CdTe DSD、0 C CdTe PAD、0-30 C JUNGFRAU 测试和 Peltier +/-0.1 C 的 I-V 平台。好处是显著降低漏电、延缓极化并允许较高偏压；代价是凝露、真空或氮气、防冷凝窗口、偏压刷新死时间、reset overshoot、温度均匀性和维护复杂度。对便携式安检或工业系统，这些代价可能比能量分辨率收益更具决定性。",
        ],
        ["kosciesza2013", "montemont2013", "cline2024", "baussens2022", "bettelli2023", "minami2023", "franklin2024", "meyer2022", "principato2012"],
    ),
    (
        "XRD/EDXRD 与公司技术路线",
        [
            "CEA-Leti/Morpho/Smiths Detection 的 XDi 路线代表产品化 EDXRD 安检系统。其核心选择是像素化 CdZnTe 模块、室温/轻度恒温、可替换模块和系统级标定。文献披露的 22 +/- 1 C、0.1 keV/C、2.26 keV @59.5 keV 等指标说明，该系统将温控作为谱峰一致性和长期可维护性的工具，而不是把探测器推向极限能量分辨率。",
            "Duke/Redlen coded-aperture/coherent scatter 路线代表算法和几何编码驱动的 XRD 系统。Greenberg 2014 的模型显示，能量分辨率从 7 keV 改善到 2.5 keV 可显著降低重建 MSE；Greenberg 2016 的 Redlen CZT 探测器在中通量 coherent scatter 中面临 ASIC 发热、CZT 温度敏感性和热/结构隔离问题。Stryker 2021 的 fan-beam 样机虽然使用能量积分平板而非 CdZnTe/CdTe，但它说明系统速度、SNR 和 q 分辨率是最终约束；若未来换成 CdZnTe/CdTe 能谱探测器，温控会直接进入速度和谱准确性的权衡。",
            "Redlen/Canon 与 eV Products/Kromek 线索共同说明 CdZnTe 的商业化高通量路线。前者在 HEXITEC、同步辐射和 high-flux 材料均匀性中体现为 Redlen HF-CZT；后者在 Prokesch 和 Bale/Szeles 中体现为 THM CdZnTe 和高通量极化模型。Acrorad 则是 CdTe 对照文献的主要材料来源，其优势是成熟 CdTe Schottky/ohmic 器件和高效率，弱点是低温、偏压刷新和极化历史管理更重。ESRF/IMEM-CNR/Bettelli/Baussens 线索显示，接触工程正在把 high-flux CdZnTe 推向同步辐射/FEL 的极高通量直接探测。",
        ],
        ["kosciesza2013", "montemont2013", "greenberg2014", "greenberg2016", "stryker2021", "prokesch2016", "bale2008", "veale2020", "baussens2022", "bettelli2023", "astromskas2016", "meyer2022"],
    ),
    (
        "综合判断",
        [
            "第一，CdZnTe 更适合室温或轻度控温稳定工作，尤其当材料为空穴输运优化的 high-flux CdZnTe 且接触工程足够好时。温控的主要目标是稳定 ASIC、漏电、基线、峰位和多模块标定；在高通量极限下，温度仍通过空穴退俘获和空间电荷影响 critical flux，但单纯降温不是替代材料和接触工程的解法。",
            "第二，CdTe 尤其 Schottky CdTe 更依赖低温、TEC/水冷、氮气或真空、防凝露和 bias refresh。温度对 CdTe 的影响不仅是漏电和噪声，还直接改变深受主退俘获、空间电荷建立、depletion width、峰位漂移和像素均匀性。0 C 与 30 C 之间的差异可以表现为数小时稳定与几十分钟极化的差异。",
            "第三，降温不等于性能单调提升。对 CdTe，降温通常降低漏电并延缓极化，但可能延长浅陷阱 persistence 或增加系统死时间和工程复杂度；对 CdZnTe，高通量稳定性常由空穴 mu-tau、偏压、厚度、接触注入、阈值和 ASIC 校正共同决定。最优温度应定义为工程最优区间：在可接受的功耗、体积、凝露风险和维护成本下，使峰位、分辨率、阈值、漏电和计数率在目标采集时间内足够稳定。",
            "第四，对于 XRD/EDXRD 和能谱成像系统，温控方案应从应用通量和运行方式反推。安检 EDXRD 可优先采用 CdZnTe 室温模块化路线；中通量 coded-aperture/coherent scatter 需要关注能量分辨率、ASIC 热隔离和中等计数率谱尾；同步辐射或高通量 photon-counting 必须使用 high-flux CdZnTe、优化接触和实时基线/漏电校正。CdTe 可作为高效率和高速特定场景的选择，但必须把低温、偏压刷新和历史效应纳入系统级误差预算。",
        ],
        ["greiffenberg2025", "bale2008", "prokesch2016", "kosciesza2013", "greenberg2016", "franklin2024", "meyer2022"],
    ),
]


tables = {
    "material": [
        ["材料/路线", "典型温度", "主要收益", "主要代价"],
        ["CdZnTe XDi/EDXRD", "22 +/- 1 C 或 25 C", "峰位一致、多模块可标定、替代 Ge 深冷", "冷却板、传感器、凝露和系统标定"],
        ["Redlen/eV high-flux CdZnTe", "18-30 C, 常见 20 C", "高偏压低漏电、ASIC/基线稳定、高通量抗极化", "Peltier/chiller/氮气/除湿、体积功耗增加"],
        ["Acrorad CdTe Schottky", "-20 C 到 0 C 常见", "降低漏电、延缓极化、允许高偏压", "TEC/水冷、真空或氮气、防凝露、bias reset 死时间"],
    ],
    "evidence": [
        ["证据类型", "CdZnTe", "CdTe"],
        ["极化机制", "trapped holes under high flux create field pinch; critical flux ~ V^2 and depends on T", "deep acceptor detrapping creates space charge; temperature strongly controls time constant"],
        ["稳定温区", "room/near-room operation often possible with contact and ASIC control", "low temperature often needed for Schottky devices under long bias"],
        ["工程重点", "hole transport, contacts, high bias, baseline correction", "TEC/water cooling, nitrogen/vacuum, bias refresh, dose history"],
    ],
}


figure_entries = [
    ("F01", "kosciesza2013", "CdZnTe", "output/important_pages/Kosciesza_2013_X_ray_diffraction_imaging_system_for_the_detection_of_illicit_substances_us_p03.png", "CEA-Leti/Morpho XDi system module and 22 +/- 1 C operating condition.", "Shows why XDi uses near-room-temperature CdZnTe control instead of cooled Ge."),
    ("F02", "montemont2013", "CdZnTe", "output/important_pages/Mont_mont_2013_An_autonomous_CZT_module_for_X_ray_diffraction_imaging_p02.png", "Autonomous CZT module architecture, detector/ASIC chain and room-temperature module concept.", "Supports the module-level engineering route for EDXRD baggage screening."),
    ("F03", "greenberg2016", "CdZnTe", "output/important_pages/Greenberg_2016_High_precision_medium_flux_rate_CZT_spectroscopy_for_coherent_scatter_imagi_p03.png", "Duke/Redlen medium-flux CZT detector layout and thermal/structural isolation idea.", "Connects detector temperature sensitivity with coherent scatter system design."),
    ("F04", "stryker2021", "Not CdZnTe/CdTe", "output/important_pages/Stryker_2021_X_ray_fan_beam_coded_aperture_transmission_and_diffraction_imaging_for_fast_m_p02.png", "Fan-beam coded-aperture XRD prototype geometry using an energy-integrating flat panel.", "Application benchmark: useful for discussing what CdZnTe/CdTe would need to replace."),
    ("F05", "veale2020", "CdZnTe", "output/important_pages/Veale_2020_Characterization_of_the_Uniformity_of_High_Flux_CdZnTe_Material_p08.png", "Redlen HF-CdZnTe/HEXITEC 241Am spectrum and FWHM uniformity maps.", "Supports near-room-temperature CdZnTe spectral-resolution stability and spatial uniformity."),
    ("F06", "cline2024", "CdZnTe", "output/important_pages/Cline_2024_Characterisation_of_Redlen_HF_CdZnTe_at_10_6_ph_s_1_mm_2_using_HEXITEC_MHz_p09.png", "HEXITEC MHz calibrated high-gain CSD spectrum at 20 keV with Gaussian fit.", "Shows high-flux CdZnTe can retain spectroscopic resolution after calibration."),
    ("F07", "cline2024", "CdZnTe", "output/important_pages/Cline_2024_Characterisation_of_Redlen_HF_CdZnTe_at_10_6_ph_s_1_mm_2_using_HEXITEC_MHz_p15.png", "Al attenuation protocol and flux-dependent 0-gamma peak-position shift.", "Shows that high-flux CdZnTe still needs leakage/baseline correction at high flux."),
    ("F08", "bale2008", "CdZnTe", "output/important_pages/supplement1/Bale_Szeles_2008_PRB_CdZnTe_high_flux_polarization_p06-06.png", "PRB model: trapped-hole space charge creates field pinch and changes electron transport.", "Mechanistic figure for CdZnTe high-flux polarization."),
    ("F09", "bale2008", "CdZnTe", "output/important_pages/supplement1/Bale_Szeles_2008_PRB_CdZnTe_high_flux_polarization_p14-14.png", "Experimental validation of critical flux dependence on bias and temperature.", "Supports V^2 dependence and exponential temperature dependence of critical flux."),
    ("F10", "thomas2017", "CdZnTe", "output/important_pages/supplement1/Thomas_2017_Redlen_high_flux_CdZnTe_p09-09.png", "Redlen HF-CdZnTe pulse shapes, spectra versus bias, and Hecht charge-collection fit.", "Shows bias-dependent charge collection and transport evidence under controlled CdZnTe operation."),
    ("F11", "prokesch2016", "CdZnTe", "output/important_pages/supplement1/Prokesch_2016_CdZnTe_100M_ph_mm2_s_p05-5.png", "Room-temperature high-flux CdZnTe count response and non-polarizing behavior.", "Key evidence for CdZnTe operation at very high photon flux near room temperature."),
    ("F12", "baussens2022", "CdZnTe", "output/important_pages/supplement1/Baussens_2022_HF_CdZnTe_optimized_electrodes_p05-05.png", "20 C dark-current I-V of optimized Redlen HF-CdZnTe contacts.", "Shows contact engineering lowers leakage and enables high bias."),
    ("F13", "baussens2022", "CdZnTe", "output/important_pages/supplement1/Baussens_2022_HF_CdZnTe_optimized_electrodes_p09-09.png", "High-flux stability/hysteresis behavior up to synchrotron-relevant fluxes.", "Shows upper flux boundary and residual field-evolution effects."),
    ("F14", "bettelli2023", "CdZnTe", "output/important_pages/supplement1/Bettelli_2023_Pt_contacts_HF_CdZnTe_p08-08.png", "Pt/CdTeO3/CZT interface and spectroscopic/contact-performance evidence.", "Explains why contact engineering, not only cooling, controls HF-CdZnTe leakage."),
    ("F15", "greiffenberg2025", "CdTe; CdZnTe", "output/important_pages/Greiffenberg_2025_Signal_stability_of_high_Z_sensors_at_synchrotron_light_sources_p09.png", "Redlen high-flux CdZnTe signal stability at 0/15/30 C and high flux.", "Direct material comparison evidence favoring CdZnTe stability."),
    ("F16", "greiffenberg2025", "CdTe; CdZnTe", "output/important_pages/Greiffenberg_2025_Signal_stability_of_high_Z_sensors_at_synchrotron_light_sources_p14.png", "CdTe Schottky continuous-illumination instability and bias-refresh comparison.", "Contrasts CdTe transient instability with CdZnTe stability."),
    ("F17", "toyama2006", "CdTe", "output/important_pages/supplement1/Toyama_2006_CdTe_polarization_quantitative_p04-4.png", "CdTe temperature-dependent barrier lowering and detrapping-time table.", "Quantitative support for temperature-controlled CdTe polarization time constants."),
    ("F18", "toyama2006", "CdTe", "output/important_pages/supplement1/Toyama_2006_CdTe_polarization_quantitative_p06-6.png", "Modified CdTe field-distribution model and 59.5 keV photopeak shift onset.", "Links electric-field evolution to peak-position drift."),
    ("F19", "principato2012", "CdTe", "output/important_pages/supplement1/Principato_2012_Al_p_CdTe_Pt_time_dependent_IV_p04-4.png", "Al/p-CdTe/Pt I-V curves as a function of temperature and measurement delay.", "Shows CdTe leakage/current data depend on temperature and time after bias."),
    ("F20", "principato2012", "CdTe", "output/important_pages/supplement1/Principato_2012_Al_p_CdTe_Pt_time_dependent_IV_p07-7.png", "Activation energy and polarization time versus temperature.", "Supports cooling as a way to increase CdTe polarization time."),
    ("F21", "cola2009", "CdTe", "output/important_pages/supplement1/Cola_Farella_2009_CdTe_Schottky_polarization_mechanism_p03-3.png", "Arrhenius analysis of CdTe Schottky polarization time constants.", "Mechanistic support for thermally activated CdTe polarization."),
    ("F22", "meyer2022", "CdTe", "output/important_pages/supplement1/Meyer_2022_CdTe_Schottky_radiation_damage_20keV_p09-09.png", "CdTe Schottky normalized hit maps after 5 h at 0/15/30 C.", "Strong visual evidence of CdTe polarization acceleration with temperature."),
    ("F23", "meyer2022", "CdTe", "output/important_pages/supplement1/Meyer_2022_CdTe_Schottky_radiation_damage_20keV_p12-12.png", "CdTe leakage-current increase versus time and temperature.", "Shows leakage current as a temperature-dependent stability metric."),
    ("F24", "astromskas2016", "CdTe", "output/important_pages/supplement1/Astromskas_2016_Schottky_CdTe_Medipix3RX_polarization_p05-5.png", "Schottky CdTe Medipix3RX polarization/tri-phase pixel and reset behavior.", "Supports the need for bias-reset scheduling and flat-field control."),
    ("F25", "becker2017", "CdTe", "output/important_pages/supplement1/Becker_2017_hole_collecting_Schottky_CdTe_sub_microsecond_p06-06.png", "Hole-collecting Schottky CdTe persistence after shutter closure and decay time constant from -30 C to +20 C.", "Shows cooling can reduce leakage/polarization yet lengthen some delayed-response time scales."),
    ("F26", "franklin2024", "CdTe", "output/important_pages/Franklin_2024_Characterizing_electron_collecting_CdTe_for_use_in_a_77_ns_burst_rate_imager_p05.png", "Electron-collecting CdTe polarization under flood illumination as a function of bias and temperature, with before/after response maps.", "Shows lower temperature and higher bias delay CdTe polarization and preserve response uniformity."),
    ("F27", "minami2023", "CdTe", "output/important_pages/Minami_2023_2_mm_thick_large_area_CdTe_double_sided_strip_detectors_for_high_resolution_sp_p06.png", "Large-area CdTe DSD reconstructed spectra at -20 C and 500 V, with text reporting <1% energy-resolution change over 20 h.", "Example of low-temperature CdTe operation for stable high-resolution spectroscopy."),
    ("F28", "greenberg2014", "CdZnTe", "output/important_pages/Greenberg_2014_CZT_detector_modeling_for_coded_aperture_X_ray_diffraction_imaging_applicat_p02.png", "CAXI model results showing reconstruction error dependence on CZT detector energy resolution and spectrum tailing.", "Connects detector energy-resolution/charge-sharing limits with coded-aperture XRD material-reconstruction quality."),
    ("F29", "cline2024", "CdZnTe", "output/important_pages/Cline_2024_Characterisation_of_Redlen_HF_CdZnTe_at_10_6_ph_s_1_mm_2_using_HEXITEC_MHz_p18.png", "Spatial maps of X-ray flux, 0-gamma peak-position shift, and dark-corrected spectra in high-flux HEXITEC MHz CdZnTe.", "Shows the spatially local nature of excess leakage-current and baseline-shift effects under high flux."),
    ("F30", "baussens2022", "CdZnTe", "output/important_pages/supplement1/Baussens_2022_HF_CdZnTe_optimized_electrodes_p06-06.png", "20 keV pulsed irradiation of optimized Redlen HF-CdZnTe with flux steps up to 8.1e9 ph mm^-2 s^-1 and R^2 = 0.9999 linearity.", "Shows high-flux CdZnTe linearity and stability under controlled 20 C synchrotron irradiation."),
    ("F31", "veale2020", "CdZnTe", "output/important_pages/Veale_2020_Characterization_of_the_Uniformity_of_High_Flux_CdZnTe_Material_p17.png", "Redlen HF-CdZnTe 12 h stability at 28 C and 18 C: counts, charge sharing, centroid, and FWHM.", "Direct evidence for near-room-temperature CdZnTe temporal stability and the modest benefit of 18 C cooling."),
    ("F32", "astromskas2016", "CdTe", "output/important_pages/supplement1/Astromskas_2016_Schottky_CdTe_Medipix3RX_polarization_p02-2.png", "Schottky CdTe/Medipix3RX count loss versus time at 12/18/24 C and at different photon fluxes.", "Shows CdTe polarization accelerates with temperature and flux."),
    ("F33", "astromskas2016", "CdTe", "output/important_pages/supplement1/Astromskas_2016_Schottky_CdTe_Medipix3RX_polarization_p06-6.png", "Optimal operational condition charts and bias-reset cycles for Schottky CdTe/Medipix3RX.", "Shows the engineering tradeoff between flux, temperature, reset off-time, and stable CdTe operation."),
]


def cite(keys):
    return "[" + ", ".join(str(1 + [r[0] for r in refs].index(k)) for k in keys) + "]"


def ref_number(key):
    return 1 + [r[0] for r in refs].index(key)


def ref_short(key):
    for item_key, authors, *_ in refs:
        if item_key == key:
            return f"[{ref_number(key)}] {authors}"
    return key


def tex_escape(s):
    return (
        s.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def write_tex():
    tex = []
    tex.append(dedent(r"""
    \documentclass[UTF8,zihao=-4]{ctexart}
    \usepackage[a4paper,margin=2.4cm]{geometry}
    \usepackage{booktabs}
    \usepackage{longtable}
    \usepackage{hyperref}
    \usepackage{graphicx}
    \usepackage{float}
    \usepackage{caption}
    \usepackage{enumitem}
    \hypersetup{colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue}
    \setlength{\parindent}{2em}
    \setlength{\parskip}{0.35em}
    \title{温度对 CdZnTe/CdTe X 射线能量分辨探测器性能影响的文献综述\\\large 面向 XRD/EDXRD、coherent scatter imaging 与相关能谱成像}
    \author{本地文献综述草稿}
    \date{\today}
    \begin{document}
    \maketitle
    \begin{abstract}
    本文基于已精读的本地文献，综述温度对 CdZnTe 和 CdTe X 射线能量分辨探测器的影响，并将讨论限定在 XRD/EDXRD、coded-aperture XRD、coherent scatter imaging、光子计数、高通量同步辐射和相关能谱成像应用。综述强调温度通过漏电流、电子噪声、能量分辨率、峰位漂移、极化、计数率能力和长期稳定性影响系统性能；同时比较 CEA-Leti/Morpho/Smiths、Duke/Redlen、Redlen/Canon、eV Products/Kromek、Acrorad、ESRF/IMEM-CNR 等路线中的温控工程权衡。
    \end{abstract}
    """))
    for title, paras, keys in sections:
        tex.append("\\section{" + tex_escape(title) + "}\n")
        for p in paras:
            tex.append(tex_escape(p) + "~\\cite{" + ",".join(keys) + "}.\n\n")
    tex.append("\\section{温控路线对比表}\n")
    for name, rows in tables.items():
        tex.append("\\begin{center}\\begin{tabular}{p{0.22\\linewidth}p{0.20\\linewidth}p{0.27\\linewidth}p{0.24\\linewidth}}\\toprule\n")
        for i, row in enumerate(rows):
            tex.append(" & ".join(tex_escape(x) for x in row) + " \\\\\n")
            tex.append("\\midrule\n" if i == 0 else "")
        tex.append("\\bottomrule\\end{tabular}\\end{center}\n\n")
    tex.append("\\section{关键图像证据目录}\n")
    tex.append("\\begin{longtable}{p{0.08\\linewidth}p{0.20\\linewidth}p{0.16\\linewidth}p{0.46\\linewidth}}\\toprule\n")
    tex.append("图号 & 文献 & 材料 & 综述作用 \\\\\\midrule\n\\endhead\n")
    for fid, refkey, material, file_path, content, role in figure_entries:
        tex.append(
            tex_escape(fid)
            + " & "
            + tex_escape(refkey)
            + f" \\cite{{{refkey}}}"
            + " & "
            + tex_escape(material)
            + " & "
            + tex_escape(role)
            + " \\\\\n"
        )
    tex.append("\\bottomrule\\end{longtable}\n\n")
    tex.append("\\section{关键实验图像证据}\n")
    for fid, refkey, material, file_path, content, role in figure_entries:
        caption = f"{fid}. {content} 综述作用: {role} 材料: {material}."
        tex.append("\\begin{figure}[H]\n\\centering\n")
        tex.append("\\includegraphics[width=0.92\\linewidth]{" + tex_escape(Path(file_path).as_posix()) + "}\n")
        tex.append("\\caption{" + tex_escape(caption) + f" 参考文献: \\cite{{{refkey}}}." + "}\n\\end{figure}\n\n")
    tex.append("\\section*{参考文献注释}\n\\begin{enumerate}[leftmargin=2.5em]\n")
    for key, authors, title, venue, material, note in refs:
        tex.append("\\item \\label{ref:" + key + "} " + tex_escape(f"{authors}. {title}. {venue}. 材料: {material}. 注释: {note}") + "\n")
    tex.append("\\end{enumerate}\n\\end{document}\n")
    (OUT / "temperature_detector_review.tex").write_text("".join(tex), encoding="utf-8")


def write_bib():
    bib = []
    for key, authors, title, venue, material, note in refs:
        year = "".join(ch for ch in authors if ch.isdigit())[-4:] or "2026"
        bib.append(
            f"@misc{{{key},\n"
            f"  author = {{{authors}}},\n"
            f"  title = {{{title}}},\n"
            f"  year = {{{year}}},\n"
            f"  note = {{{venue}; material: {material}; {note}}}\n"
            f"}}\n\n"
        )
    (OUT / "references.bib").write_text("".join(bib), encoding="utf-8")


def write_figure_catalog():
    header = ["figure_id", "reference_key", "reference_no", "material", "image_file", "what_it_shows", "role_in_review", "inserted"]
    lines = ["\t".join(header)]
    for fid, refkey, material, file_path, content, role in figure_entries:
        lines.append("\t".join([fid, refkey, str(ref_number(refkey)), material, file_path, content, role, "yes"]))
    (OUT / "figure_catalog.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def register_fonts():
    font_path = Path(r"C:\Windows\Fonts\NotoSerifSC-VF.ttf")
    bold_path = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("CN", str(font_path)))
        pdfmetrics.registerFont(TTFont("CNBold", str(bold_path if bold_path.exists() else font_path)))
        return "CN", "CNBold"
    font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
    pdfmetrics.registerFont(TTFont("CN", str(font_path)))
    pdfmetrics.registerFont(TTFont("CNBold", str(font_path)))
    return "CN", "CNBold"


def write_pdf():
    font, bold = register_fonts()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CNTitle", fontName=bold, fontSize=18, leading=25, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="CNSubTitle", fontName=font, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.darkgrey, spaceAfter=18))
    styles.add(ParagraphStyle(name="CNHeading", fontName=bold, fontSize=13.5, leading=19, spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle(name="CNBody", fontName=font, fontSize=9.7, leading=16.8, alignment=TA_LEFT, firstLineIndent=18, spaceAfter=6))
    styles.add(ParagraphStyle(name="CNRef", fontName=font, fontSize=8.2, leading=12.2, alignment=TA_LEFT, spaceAfter=3))
    styles.add(ParagraphStyle(name="CNTable", fontName=font, fontSize=7.6, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="CNTableHead", fontName=bold, fontSize=7.8, leading=10.5, alignment=TA_CENTER))

    pdf_path = writable_pdf_path()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=2.1 * cm,
        leftMargin=2.1 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
    )
    story = [
        Paragraph("温度对 CdZnTe/CdTe X 射线能量分辨探测器性能影响的文献综述", styles["CNTitle"]),
        Paragraph("面向 XRD/EDXRD、coherent scatter imaging 与相关能谱成像", styles["CNSubTitle"]),
        Paragraph("摘要", styles["CNHeading"]),
        Paragraph("本文基于已精读的本地文献，综述温度对 CdZnTe 和 CdTe X 射线能量分辨探测器的影响。重点不是 XRD 衍射物理本身，而是温度如何通过漏电流、电子噪声、能量分辨率、峰位漂移、极化、计数率能力和长期稳定性影响 XRD/EDXRD、coded-aperture XRD、coherent scatter imaging、光子计数和高通量 X 射线能谱成像系统。", styles["CNBody"]),
    ]
    for title, paras, keys in sections:
        story.append(Paragraph(title, styles["CNHeading"]))
        for p in paras:
            story.append(Paragraph(p + " " + cite(keys), styles["CNBody"]))
    story.append(Paragraph("温控路线对比表", styles["CNHeading"]))
    for table_index, rows in enumerate(tables.values()):
        if table_index > 0:
            story.append(PageBreak())
        data = []
        for i, row in enumerate(rows):
            st = styles["CNTableHead"] if i == 0 else styles["CNTable"]
            data.append([Paragraph(x, st) for x in row])
        t = Table(data, colWidths=[3.2 * cm, 3.0 * cm, 4.6 * cm, 4.4 * cm], repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEFF7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
    story.append(PageBreak())
    story.append(Paragraph("关键图像证据目录", styles["CNHeading"]))
    catalog_data = [[Paragraph(x, styles["CNTableHead"]) for x in ["图号", "文献", "材料", "综述作用"]]]
    for fid, refkey, material, file_path, content, role in figure_entries:
        catalog_data.append([
            Paragraph(fid, styles["CNTable"]),
            Paragraph(f"{refkey} [{ref_number(refkey)}]", styles["CNTable"]),
            Paragraph(material, styles["CNTable"]),
            Paragraph(role, styles["CNTable"]),
        ])
    ct = Table(catalog_data, colWidths=[1.2 * cm, 3.0 * cm, 2.5 * cm, 8.5 * cm], repeatRows=1)
    ct.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEFF7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(ct)
    story.append(PageBreak())
    story.append(Paragraph("关键实验图像证据", styles["CNHeading"]))
    for fig_index, (fid, refkey, material, file_path, content, role) in enumerate(figure_entries):
        if fig_index > 0:
            story.append(PageBreak())
        img_path = ROOT / file_path
        if not img_path.exists():
            story.append(Paragraph(f"{fid}: missing image {file_path}", styles["CNRef"]))
            continue
        reader = ImageReader(str(img_path))
        iw, ih = reader.getSize()
        max_w, max_h = 15.4 * cm, 15.4 * cm
        scale = min(max_w / iw, max_h / ih)
        story.append(Paragraph(f"{fid} | {refkey} | {material} | 参考文献 {ref_short(refkey)}", styles["CNHeading"]))
        story.append(Image(str(img_path), width=iw * scale, height=ih * scale))
        story.append(Paragraph(content + " 综述作用: " + role + f" 参考文献: {ref_short(refkey)}.", styles["CNRef"]))
        story.append(Spacer(1, 8))
    story.append(PageBreak())
    story.append(Paragraph("参考文献注释", styles["CNHeading"]))
    for idx, (key, authors, title, venue, material, note) in enumerate(refs, start=1):
        story.append(Paragraph(f"[{idx}] {authors}. {title}. {venue}. 材料: {material}. 注释: {note}", styles["CNRef"]))

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont(font, 8)
        canvas.drawCentredString(A4[0] / 2, 1.15 * cm, f"{doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return pdf_path


if __name__ == "__main__":
    write_tex()
    write_bib()
    write_figure_catalog()
    pdf_path = write_pdf()
    print(OUT / "temperature_detector_review.tex")
    print(OUT / "references.bib")
    print(OUT / "figure_catalog.tsv")
    print(pdf_path)
