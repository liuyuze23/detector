# 本地文献深度分析：CdZnTe/CdTe 探测器温度性能、温控方案与 XRD/EDXRD 应用

工作区：`C:\Users\Yuze Liu\Desktop\探测器`

本轮只分析本地已有 10 篇 PDF。重点不是泛泛讲 XRD，而是抽取与“温度-探测器性能-温控工程-XRD/EDXRD/能谱成像样机-公司路线”直接相关的信息。重要实验图已按整页 PNG 保存到 `output/important_pages/`，便于后续核对图题、坐标轴和实验上下文。

## 0. 总体判断

1. 本地文献已经覆盖三条核心证据链：
   - Redlen/HEXITEC/高通量 CdZnTe：说明 HF-CdZnTe 可在室温或轻度控温下长时间稳定工作，但高通量下仍可能出现局域、通量相关的“excess leakage-current”或类极化现象。
   - CEA-Leti/Morpho XDi/IMADIF：说明 XRD/EDXRD 安检系统为何选择室温 CZT 模块替代低温 Ge，并给出明确温控设定 22±1 C、20-25 C 工作范围、峰位漂移 0.1 keV/C。
   - Duke/Redlen coded-aperture coherent scatter：说明 coded-aperture XRD 对 CZT 的能量分辨率和中通量能力要求，且指出实际系统速度受探测器噪声/能量敏感读出约束。

2. CdZnTe 与 CdTe 的温度响应差异在本地文献中很清楚：
   - CdZnTe，尤其 Redlen HF-CdZnTe，更强调室温稳定、免低温/免周期偏压刷新、可在高通量下抑制传统极化。温控的主要目标往往是稳定 ASIC、基线和能量标定，而不是必须低温才能工作。
   - CdTe，尤其 Schottky CdTe，更依赖低温、高偏压、真空/TEC 与偏压刷新/恢复策略来延缓极化、降低漏电并维持均匀性。降温通常有利，但不是充分条件：高通量/长时间照射下仍可能出现信号衰减、响应不均匀和极化图案。

3. “降温一定提升性能”不能作为结论。更准确的判断是：
   - 降温通常降低热激发漏电流和电子噪声，有助于峰位/基线稳定，尤其对 CdTe 更明显。
   - 但过低温度会带来凝露风险、TEC 功耗、热梯度、机械体积、封装复杂度和便携性下降；并且部分陷阱/去陷阱动力学并非单调有利。高通量 CdZnTe 文献中更常采用 18-28 C、20 C 或 22±1 C 这种“工程控温”而非深冷。

## 1. Redlen HF-CdZnTe + HEXITEC：室温稳定与高通量新问题

### 1.1 Veale et al. 2020, Characterization of the Uniformity of High-Flux CdZnTe Material

图像证据：F05（CdZnTe，241Am 能谱与 FWHM 均匀性图，用于说明 Redlen HF-CdZnTe 近室温能谱性能与空间均匀性）；F31（CdZnTe，28 C 与 18 C 下 12 h counts、charge sharing、peak centroid、FWHM 稳定性，用于说明轻度降温带来的长期稳定性改善）。

本地 PDF：`Veale 等 - 2020 - Characterization of the Uniformity of High-Flux CdZnTe Material.pdf`

相关性：极高。它是 Redlen HF-CdZnTe 与 STFC HEXITEC 的核心材料表征论文，给出室温、偏压、能量分辨率、长期稳定性、CdTe 对照和参考文献索引。

材料与结构：
   - Redlen Technologies 生长和加工 HF-CdZnTe。
   - 10 个 20.35 mm x 20.45 mm x 2.00 mm 传感器。
   - 80 x 80 像素，250 um pitch，flip-chip 到 STFC HEXITEC ASIC。
   - HEXITEC GigE DAQ，帧率 1.6 kHz。

温度/温控：
   - DAQ 提供温度控制系统，使 ASIC 保持室温 28 C。
   - 主要测试在 28 C；长期稳定性对比 28 C 与 18 C。
   - 这不是深冷路线，而是稳定 ASIC/探测器工作点的室温或轻度降温路线。

偏压与计数条件：
   - 默认偏压 750 V，即 325 V/mm。
   - 长期稳定性测试中恒定偏压，无 bias refresh。
   - 241Am 平场源，约 3 x 10^3 ph s^-1 mm^-2，300 s/次；长期测试为 300 s 采集，每 900 s 一次，总 9-12 h。

能量分辨率：
   - 10 个器件在 59.54 keV 的平均 FWHM 为 0.83 keV。
   - 单个优秀器件 D185735：59.54 keV 平均 FWHM 0.79±0.15 keV；最佳像素可低至 0.54 keV。
   - 13.94 keV FWHM 0.61±0.13 keV。
   - 99.93% 像素 FWHM < 2 keV。

温度与长期稳定性：
   - D185735 在 28 C 和 18 C、750 V 恒偏下测试 9-12 h。
   - FWHM 漂移：28 C 下约 770 eV -> 840 eV；18 C 下约 760 eV -> 780 eV。
   - 作者认为这些变化很小，无明显空间相关性，说明 HF-CdZnTe 具有多小时稳定性。
   - 18 C 的 FWHM 漂移明显更小，但论文没有把 18 C 描述为必须条件；28 C 也足以支撑典型运行。

CdZnTe vs CdTe 对照：
   - 文中明确说 CdZnTe 的优势之一是不同于 CdTe，不需要周期性 bias cycling 来避免 bias-induced polarization。
   - Redlen HF-CdZnTe 的空间均匀性可与 Acrorad Schottky CdTe 相比，最佳器件像素计数变化 <6%。

极化与温度解释：
   - 传统 CZT 高通量下会因空穴寿命短、空穴俘获造成极化。
   - HF-CdZnTe 通过优化空穴寿命，降低/抑制高通量极化。
   - 文中梳理两类极化：flux-induced polarization 与 bias-induced polarization；影响因素包括 photon flux、电极类型、偏压和温度。
   - CdTe Schottky 常需要 bias refresh：偏压周期性降到 0 V 约 1 s，使空间电荷复合，刷新周期可为分钟到小时级。

对综述的价值：
   - 支撑“Redlen HF-CdZnTe 可室温稳定运行，温控主要服务于稳定性而非深冷”的核心判断。
   - 支撑“低温可降低长期漂移，但轻度降温已经足够，且不必像 Ge 或 CdTe 那样强依赖复杂制冷”的判断。

已保存重要图页：
   - `output/important_pages/Veale_2020_Characterization_of_the_Uniformity_of_High_Flux_CdZnTe_Material_p01.png`：摘要与材料/性能概览。
   - `..._p04.png`：DAQ 温控、28 C、750 V、CdTe 需要 bias cycling 的关键段落。
   - `..._p08.png` / `..._p09.png`：能量分辨率图与 10 个器件表。
   - `..._p15.png` / `..._p16.png` / `..._p17.png`：极化讨论、28 C vs 18 C 长期稳定性、FWHM/峰位变化图。

应继续追索参考文献：
   - Thomas et al., Characterisation of Redlen high-flux CdZnTe, JINST 2017, 12, C12045。优先级最高，Redlen HF-CZT 早期高通量材料论文。
   - Bale, Soldner, Szeles, A mechanism for dynamic lateral polarization in CdZnTe under high flux X-ray irradiation, Appl. Phys. Lett. 2008, 92, 082101。极化机理论文。
   - Prokesch et al., CdZnTe Detectors Operating at X-ray Fluxes of 100 Million Photons/(mm2.sec), IEEE TNS 2016。高通量 CZT。
   - Cola & Farella, The polarization mechanism in CdTe Schottky detectors, Appl. Phys. Lett. 2009。CdTe 极化机理。
   - Astromskas et al., Evaluation of Polarization effects of e-Collection Schottky CdTe Medipix3RX Hybrid Pixel Detector, IEEE TNS 2016。CdTe/Medipix 对照。
   - Wilson et al., A 10 cm x 10 cm CdTe Spectroscopic Imaging Detector based on the HEXITEC ASIC, JINST 2015。HEXITEC CdTe 大面积系统。

### 1.2 Cline et al. 2024, Characterisation of Redlen HF-CdZnTe at >10^6 ph s^-1 mm^-2 using HEXITEC MHz

图像证据：F06（CdZnTe，20 keV high-gain CSD 谱峰 Gaussian fit，用于说明 HEXITEC MHz 校准后仍可保持高通量能谱分辨）；F07（CdZnTe，Al 衰减片切换与 0-gamma peak-position shift 曲线，用于说明高通量下局域漏电/基线漂移）；F29（CdZnTe，X-ray flux map、0-gamma shift map 与 dark-corrected spectra，用于说明 excess leakage-current/baseline shift 的空间局域性）。

本地 PDF：`Cline 等 - 2024 - Characterisation of Redlen HF-CdZnTe at  10 6 ph s -1 mm -2 using HEXITEC MHz.pdf`

相关性：极高。它把 Redlen HF-CdZnTe 推到 MHz 连续成像和 >10^6 ph s^-1 mm^-2 通量，直接暴露“高通量下不是传统极化但仍有局域漏电/基线漂移”的新问题。

材料与结构：
   - Redlen HF-CZT，2 mm 厚，20.35 mm x 20.35 mm。
   - 80 x 80 像素，250 um pitch，25 um inter-pixel gap。
   - Pt electrodes，planar cathode + pixelated anode。
   - Hybridised to HEXITECMHz ASIC，连续 1 MHz frame rate。

温度/温控：
   - LOKI/PCB 传感器监测温度与湿度。
   - 探测器安装在 Peltier 上，位于 humidity-controlled enclosure。
   - 温度信息反馈到电源以维持稳定工作温度。
   - 主要结果在 ASIC temperature 20 C。
   - 低于环境温度运行时，外置两个 solid-state de-humidifiers 防凝露。

偏压与通量：
   - 传感器偏压 -1000 V，即 500 V/mm。
   - DLS B16 beamline，12-35 keV；典型能谱表征 20 keV。
   - 20 keV、1.83% occupancy 对应 2.93 x 10^5 ph s^-1 mm^-2。
   - 高通量动态实验达到 1.26 x 10^7 ph s^-1 mm^-2。

能量分辨率：
   - 20 keV 下，高增益平均 FWHM 850±100 eV，中增益 920±110 eV，低增益 1130±120 eV。
   - 达到连续 MHz 成像目标：<1 keV spectroscopic resolution。
   - 作者指出分辨率仍远高于 CZT Fano 极限，主要受 ASIC/电子噪声、漏电等贡献限制。

温度/漏电/峰位漂移：
   - 发现被照射像素的 0-gamma peak/baseline 向高 ADU 偏移，表现为“excess leakage-current effect”。
   - 这是局域、通量相关、动态的效应；不是 ASIC 效应，而是 HF-CZT 传感器效应。
   - 在 1.26 x 10^7 ph s^-1 mm^-2 下，典型像素 offset 为 144 ADU，等效 14.26 keV，约为低增益 300 keV 动态范围的 4.75%。
   - 同一条件等效每像素漏电流约 543 pA，即 8.68 nA/mm^2。
   - 60 keV 高增益 integration-length scan：照射像素平均漏电 31.48 pA，未照射像素 9.51 pA，额外漏电约 352 pA/mm^2；边界相邻像素差异也明显，说明高度局域。

机理解释：
   - 作者认为不是 bulk hole trapping，因为 20 keV 主要在靠近电极约 80-100 um 的区域相互作用，载流子漂移时间远短于 HF-CZT 空穴寿命。
   - 推测来自 electrode-CZT interface 陷阱，空间电荷局域积累，临时改变金属-CZT 接触势垒。
   - 论文明确说仍需不同能量、不同温度、相同通量的数据来验证温度依赖。因此它是后续研究空白的好抓手。

工程意义：
   - Peltier + 湿度控制 + 除湿是高通量 CZT 谱成像原型机的典型温控方案。
   - 温控目标不只是降低漏电，还包括稳定 ASIC、避免基线漂移、保护低于环境运行时的凝露风险。
   - 对最终用户，作者认为可由 FPGA 实时校正 offset，因此该效应未必直接破坏应用，但对高通量 XRD/EDXRD 的峰位和能量标定必须建模。

已保存重要图页：
   - `output/important_pages/Cline_2024_Characterisation_of_Redlen_HF_CdZnTe_at_10_6_ph_s_1_mm_2_using_HEXITEC_MHz_p01.png`：摘要，850 eV、543 pA、1.26e7 通量。
   - `..._p04.png`：Peltier、湿度控制、20 C、除湿防凝露。
   - `..._p09.png`：20 keV FWHM 分布与表。
   - `..._p11.png`：0-gamma peak shift/漏电效应识别。
   - `..._p14.png` / `..._p15.png`：通量依赖，144 ADU、543 pA。
   - `..._p18.png` / `..._p19.png`：integration-length scan，照射/未照射漏电流图。

应继续追索参考文献：
   - Baussens et al., Characterization of High-Flux CdZnTe with optimized electrodes for 4th generation synchrotron light sources。极高优先级，涉及 HF-CZT 在更高通量、不同电极下的类似现象。
   - Thomas et al. 2017 JINST C12045。
   - Pike et al., Properties of Redlen cadmium zinc telluride with respect to x-ray spectroscopy。
   - HEXITECMHz ASIC 相关早期论文，特别是 1 MHz 连续 X-ray imaging system。

## 2. CEA-Leti/Morpho/Smiths 路线：XDi/IMADIF 安检 XRD 模块

### 2.1 Montemont et al. 2013, An Autonomous CZT Module for X-ray Diffraction Imaging

图像证据：F02（CdZnTe，自主 CZT XDi 模块结构、detector/ASIC 链路和室温模块概念，用于说明 CEA-Leti/Morpho 模块化 EDXRD 温控路线）。

本地 PDF：`Montémont 等 - 2013 - An autonomous CZT module for X-ray diffraction imaging.pdf`

相关性：极高。它描述 CEA-Leti 为 Morpho Detection XDi 开发的 IMADIF CZT 模块，给出模块结构、室温设定、偏压、噪声、漏电和能量分辨率。

应用背景：
   - XDi 是 Morpho Detection 提出的 XRD 安检架构，用于提高衍射行李扫描吞吐量并进入 cabin baggage screening。
   - 模块设计目标是以 room-temperature CZT 替代 cooled Ge。
   - 论文明确说高吞吐系统不需要 HPGe 那样极高能量分辨率；CZT 的 few percent 分辨率足以识别衍射模式。

材料与结构：
   - 5 mm thick high-resistivity CZT。
   - 输入能量范围 20-150 keV。
   - 检测面积 660 mm^2。
   - 192 anodes + 12 cathodes，双面读出，用于 DOI、charge sharing、induction sharing 校正。
   - anode ASIC：IDeF-X HD；cathode ASIC：ALIGASPECT。
   - FPGA 实时校正 gain、offset、DOI、charge sharing，Ethernet 输出。

温度/温控：
   - 模块为 room-temperature operated CZT。
   - 性能结果处写：modules are regulated to 25 C。
   - 与 Kosciesza 系统论文共同构成 22-25 C 工程温控路线。

偏压、噪声与漏电：
   - 模拟示例：5 mm CZT biased at 700 V。
   - 实际系统选择 700 V，以平衡 shot noise 与 charge sharing degradation。
   - 500 V bias 时，电极漏电流约 0.2-1.5 nA，噪声典型 170-220 rms electrons。
   - shaping time 0.7 us，用于应对 shot noise。
   - 总 ASIC 功耗 <300 mW。

能量分辨率与效率：
   - 25 C 下平均能量分辨率：122 keV 为 2.4% FWHM，60 keV 为 3.8% FWHM。
   - 83 个探测器统计：60 keV 效率 73±4%，60 keV 分辨率 3.8±0.2%，122 keV 分辨率 2.4±0.2%。
   - 室温模块间重现性较好。

工程判断：
   - 这里的温控不是追求最佳单像素能量分辨率，而是让大规模模块阵列长期、可维护、可替换地工作在安检场景。
   - 选择 25 C 附近是系统集成折中：不需要 Ge 的真空/深冷，不需要大制冷功率，同时分辨率满足 EDXRD 物质识别。

已保存重要图页：
   - `output/important_pages/Mont_mont_2013_An_autonomous_CZT_module_for_X_ray_diffraction_imaging_p01.png`：摘要、XDi 背景、25 C 性能。
   - `..._p02.png`：5 mm CZT、700 V、漏电/噪声、IDeF-X/ALIGASPECT。
   - `..._p04.png`：83 模块统计表、系统集成到 600 bags/hour prototype。

应继续追索参考文献：
   - Harding et al., XDi 架构与 direct tomographic EDXRD imaging。
   - Cozzini et al., Energy dispersive X-ray diffraction spectral resolution considerations for security screening applications, IEEE NSS/MIC 2010。
   - IDeF-X HD ASIC 论文：Gevin et al., NIM A 695, 2012。
   - CEA-Leti CdZnTe/CdTe imaging 综述：Verger et al., New trends in gamma-ray imaging with CdZnTe/CdTe at CEA-Leti, NIM A 571, 2007。

### 2.2 Kosciesza et al. 2013, X-ray diffraction imaging system for illicit substances using pixelated CZT detectors

图像证据：F01（CdZnTe，CEA-Leti/Morpho XDi 系统模块与 22 +/- 1 C 工作条件，用于说明安检 EDXRD 系统选择近室温恒温 CZT 而非 cooled Ge 的工程原因）。

本地 PDF：`Kosciesza 等 - 2013 - X-ray diffraction imaging system for the detection of illicit substances using pixelated CZT-detectors.pdf`

相关性：极高。这是 XDi 系统论文，比模块论文更直接给出安检系统温控目的、峰位温漂与系统工程代价。

系统与应用：
   - Morpho Detection Germany + CEA-Leti。
   - XDi cabin-baggage screener，17 个 pixelated CZT detector modules。
   - 多焦点 X-ray source（MFXS），高通量，减少机械运动。
   - 系统目标：比 XRD3500 小、轻、高吞吐。表中 XRD3500 长 7 m、重 9.8 t；XDi 长 3.3 m、重 2 t。

为什么用室温 CZT 替代 Ge：
   - 需要 130 cm 宽度上分布探测面积。
   - Ge 需要低温真空容器和可靠大制冷功率；成本、体积、维护、快速更换都不适合安检点。
   - CZT 模块只需 12 V、trigger、Ethernet，完全自治，便于维护替换。

探测器结构与指标：
   - CZT 5 mm。
   - 192 pixels，22 lines。
   - Anode ASIC：IDeF-X；Cathode ASIC：ALIGASPECT。
   - 40 modules 的 59.5 keV 平均能量分辨率 2.26±0.13 keV。
   - 59.5±3 keV peak efficiency 73±4%。
   - 安装后无法用源高效标定，改用 X-ray tube tungsten K-alpha/K-beta 与 foam-cube scatter 进行系统内标定。

温度/温控：
   - 模块保持在 22±1 C。
   - 设计工作范围 20-25 C，目标 22 C。
   - 使用长冷却板从模块下方保持温度。
   - 通过改变 cooling-plate temperature（约 0.5 C 步进）产生不同模块内部温度，并用模块内 dedicated sensor 测量。

峰位温漂：
   - 平均 2175 pixels 的峰位随温度变化，得到 peak shift gradient 0.1 keV/C。
   - 结论：20-25 C 范围内温度变化可接受；不需要担忧该范围内温漂。
   - 从工程上看，22±1 C 带来的峰位变化约 0.1 keV，远低于模块平均分辨率 2.26 keV，因此稳定度足够。

对综述的价值：
   - 这是“为什么系统采用某一温度条件”的最强本地案例。
   - 说明温控的核心不是把 CZT 冷到很低，而是保证多模块阵列标定和峰位稳定。
   - 同时给出 Ge 的代价：真空容器、低温制冷、系统体积、重量、维护与快速更换困难。

已保存重要图页：
   - `output/important_pages/Kosciesza_2013_X_ray_diffraction_imaging_system_for_the_detection_of_illicit_substances_using_pixelated_CZT_detecto_p01.png`：XDi 摘要、17 CZT 模块、系统概念。
   - `..._p03.png`：room-temperature CZT 替代 Ge 的工程理由、22±1 C、模块指标表。
   - `..._p04.png`：20-25 C、冷却板、0.1 keV/C 峰位漂移图、结论。

应继续追索参考文献：
   - Harding, The design of direct tomographic energy-dispersive X-ray diffraction imaging (XDI) systems, SPIE 5923, 2005。
   - Harding and Delfs, Liquids Identification by X-ray diffraction, SPIE 6707, 2007。
   - Morpho/Smiths/Safran XDi/XRD 专利和产品材料。

## 3. Duke/Redlen coded-aperture coherent scatter/XRD：探测器指标如何限制系统

### 3.1 Greenberg, Iniewski, Brady 2014, CZT detector modeling for coded aperture X-ray diffraction imaging applications

图像证据：F28（CdZnTe，CAXI 模型中重建误差随 CZT 能量分辨率和谱尾变化的结果，用于把探测器能量分辨率/charge sharing 限制与 coded-aperture XRD 材料重建质量联系起来）。

本地 PDF：`Greenberg 等 - 2014 - CZT detector modeling for coded aperture X-ray diffraction imaging applications.pdf`

相关性：高。它不是温控实验，但直接说明 CAXI/coded aperture XRD 对 CZT 能量分辨率、计数率、像素尺寸、偏压等非理想效应的敏感性。

关键信息：
   - 作者单位：Duke University + Redlen Technologies。
   - 目标：评估 CZT energy-sensitive detectors 在 coded aperture X-ray imaging/CAXI 中的性能权衡。
   - 模型包括 charge sharing、incomplete charge collection due to DOI、K-edge escape。
   - 探测器参数包括 pixel size、detector thickness、contacts、HV bias、count rate。

能量分辨率影响：
   - 模拟 FWHM 2.5 keV、4 keV、7 keV。
   - FWHM 从 7 keV 降到 2.5 keV 可使 normalized MSE 约降低 2 倍，并改善 momentum transfer resolution。
   - 这说明在 XRD/EDXRD 中，温控若能降低电子噪声/漏电/峰位漂移，最终作用会传导到材料谱反演和 q 分辨率。

谱尾与计数率：
   - 谱尾 1%、10%、20%、50% 的影响比作者预期小，但会影响 form factor/material classification。
   - charge-sharing correction/discrimination 可降低谱尾到约 1%，但会限制最大计数率。
   - 谱尾大小与 pixel size、thickness、HV bias、mobility products、photon count rate 有关。

温度相关意义：
   - 文中没有给具体温度条件，但“HV bias、count rate、漏电/电子噪声/谱尾”都与温度相关。
   - 可作为综述中解释“为什么温控最终影响 XRD 成像质量，而不只是影响单个峰”的模型证据。

已保存重要图页：
   - `output/important_pages/Greenberg_2014_CZT_detector_modeling_for_coded_aperture_X_ray_diffraction_imaging_applications_p01.png`：摘要、模型输入参数。
   - `..._p02.png`：FWHM 2.5/4/7 keV 对 CAXI 的影响。
   - `..._p03.png`：谱尾/charge sharing/结论。

应继续追索参考文献：
   - Greenberg et al., Snapshot molecular imaging using coded energy-sensitive detection, Optics Express 2013。
   - Greenberg et al., Compressive Single-Pixel Snapshot X-ray Diffraction Imaging, Optics Letters 2014。
   - Iniewski et al., High Voltage Optimization in CZT Detectors, IEEE NSS/MIC 2008。
   - Iniewski et al., CZT Pixel Scaling for Improved Spatial Resolution in Medical Imaging, IEEE NSS/MIC 2008。

### 3.2 Greenberg et al. 2016, High precision, medium flux rate CZT spectroscopy for coherent scatter imaging

图像证据：F03（CdZnTe，Duke/Redlen medium-flux CZT 探测器几何、CZT 条带布局与热/结构隔离设计，用于说明 coherent scatter imaging 中探测器温度敏感性如何进入系统工程）。

本地 PDF：`Greenberg 等 - 2016 - High precision, medium flux rate CZT spectroscopy for coherent scatter imaging.pdf`

相关性：极高。它是 Duke/Redlen 为 coded aperture coherent scatter imaging 设计 CZT 中通量谱探测器的直接论文。

探测器目标：
   - 传统 CZT 两种模式：高精度低通量 spectroscopy，或低精度高通量 photon counting。
   - coded aperture coherent scatter 位于中间窗口：10-100 kcps/mm^2，同时需要 2-3% 或几 % 能量分辨率。
   - 目标规格：5% energy resolution at 60 keV；最大 10 kcps/mm^2。

材料/结构：
   - Redlen Technologies 合作。
   - 3 mm thick CZT。
   - 40 mm x 10 mm active detector area，由两个 20 mm x 10 mm CZT 元件拼接。
   - 80 x 20 grid，0.5 mm square pixels。
   - 为适应 fan-beam geometry 设计 2D detector。
   - ASIC 与 CZT 之间使用 interposer PCB，提供热/结构隔离，但增加 stray capacitance，损害能量分辨率。

温度/热控制线索：
   - 文中明确提到 ASIC dissipating power 与 temperature sensitive CZT 之间需要 thermal and structural isolation。
   - 没有给出具体 TEC 或温度设定。这是一个信息空白，后续应追索完整 detector build 或 Redlen/Quadridox/Duke 技术资料。

高通量/极化判断：
   - 高通量 CZT >1 Mcps/mm^2 面临 polarization；trap charge 积累可导致电场崩塌。
   - 高通量材料用改进 THM 生长、提高 hole mobility-lifetime，可实现 >100 Mcps/mm^2。
   - 但高通量探测器常用 semi-Ohmic contacts 避免极化，代价是暗电流更高、能量分辨率下降。
   - coherent scatter 的 1-100 kcps/mm^2 不需要 CT 级高通量材料，但需要比传统 spectroscopy 高几个数量级计数率。

实测性能：
   - Am-241 59.54 keV，源距约 100 mm。
   - 中央区域平均 energy resolution 5% at 60 keV，即 2.98 keV FWHM；最佳像素 3.2%，即 1.89 keV FWHM。
   - checkerboard 区域较差，6-15%。
   - 中央区域在约 500 cps/mm^2 表征，并观察到均匀结果可到约 10 kcps/mm^2 incident count rate。
   - 达成中央 800 pixels：<5% energy resolution，接近 10 kcps/mm^2。

对综述的价值：
   - 用于说明 Duke 路线的探测器要求：不是单纯追求极限 eV 分辨率，而是 60 keV 几 keV FWHM + 10 kcps/mm^2 + 2D 空间角分辨。
   - 可解释温控/热隔离为何重要：ASIC 发热会影响 CZT 基线、漏电和能量标定；interposer 隔热又带来电容和分辨率代价。

已保存重要图页：
   - `output/important_pages/Greenberg_2016_High_precision_medium_flux_rate_CZT_spectroscopy_for_coherent_scatter_imaging_p01.png`：摘要、计数率/能量分辨率窗口。
   - `..._p03.png`：高通量极化、CZT 结构。
   - `..._p04.png`：pixel/thickness/interposer 热隔离。
   - `..._p05.png`：实测计数率和 FWHM 图。

应继续追索参考文献：
   - MacCabe et al., Pencil beam coded aperture X-ray scatter imaging, Optics Express 2012。
   - Hassan et al., Snapshot fan beam coded aperture coherent scatter tomography, Optics Express 2016。
   - Lakshmanan et al., Design and implementation of coded aperture coherent scatter spectral imaging of breast tissue samples, Journal of Medical Imaging 2016。
   - Duke/Quadridox 专利：Systems and methods for tissue discrimination via multi-modality coded aperture X-ray imaging。

### 3.3 Stryker et al. 2021, X-ray fan beam coded aperture transmission and diffraction imaging for fast material analysis

图像证据：F04（非 CdZnTe/CdTe，fan-beam coded-aperture XRD 样机几何与能量积分平板探测器，用作应用样机参照，说明未来若替换为 CdZnTe/CdTe 能谱探测器需要满足的系统约束）。

本地 PDF：`Stryker 等 - 2021 - X-ray fan beam coded aperture transmission and diffraction imaging for fast material analysis.pdf`

相关性：中-高。它是 Duke fan-beam coded aperture transmission + diffraction imaging 实体样机，但使用的是商业能量积分平板，不是 CZT/CdTe 能谱探测器。必须在综述中准确区分。

系统：
   - 160 kV Bremsstrahlung X-ray source。
   - 15 x 15 cm^2 FOV，约 1 x 1 mm^2 XRD spatial resolution。
   - XRD acquisition：160 kVp、3 mA、15 s/fan slice。
   - transmission：80 kVp、6 mA、100 ms。
   - Detector：Xineos-2329, Teledyne Dalsa，active area 228 x 292 mm^2，50 um pixel pitch，采集时 bin 到 100 um。
   - Coded aperture：3 mm Cu，40% open fraction，0.75 mm features。

性能：
   - q FWHM 约 0.0095±0.0017 A^-1，q accuracy 0.002±0.001 A^-1。
   - 多个样品可 7-9 min 完成 15 x 15 cm^2 扫描。
   - 材料谱与商业 diffractometer 交叉相关可达 >95%。

探测器限制：
   - 论文讨论中明确指出当前系统速度关键限制之一是 detector noise。
   - photon-counting 或 energy-sensitive detectors 可提高 SNR、速度和分辨率，但代价是更昂贵的大面积二维能量敏感探测器。

温度相关性：
   - 本文未披露探测器温控，因为用的是能量积分平板。
   - 它的价值是说明如果未来替换成 CZT/CdTe 能谱探测器，温控将直接影响速度、SNR、q 分辨率和谱准确性。

已保存重要图页：
   - `output/important_pages/Stryker_2021_X_ray_fan_beam_coded_aperture_transmission_and_diffraction_imaging_for_fast_material_analysis_p01.png`：系统概览。
   - `..._p02.png` / `..._p03.png`：q 分辨率、15 s/fan slice。
   - `..._p08.png`：方法、源/探测器/曝光参数。

应继续追索参考文献：
   - Stryker, Kapadia, Greenberg, Simulation based evaluation of a fan beam coded aperture X-ray diffraction imaging system for biospecimen analysis, Phys. Med. Biol. 2021。
   - Greenberg & Wolter, X-ray Diffraction Imaging Technology and Applications, CRC Press 2019。
   - Hassan et al. 2016 Optics Express。

## 4. CdTe 对照：低温、高偏压、极化与稳定性

### 4.1 Minami et al. 2023, 2-mm-thick large-area CdTe double-sided strip detectors

图像证据：F27（CdTe，-20 C、500 V 下 large-area CdTe DSD 重建能谱与正文中 20 h 能量分辨率变化 <1% 的说明，用于作为低温 CdTe 稳定高分辨谱成像案例）。

本地 PDF：`Minami 等 - 2023 - 2-mm-thick large-area CdTe double-sided strip detectors for high-resolution spectroscopic imaging of.pdf`

相关性：高。它不是 XRD 专门论文，但给出 Acrorad CdTe 厚探测器在低温、高偏压下避免极化并稳定能谱成像的明确例子。

材料与结构：
   - 2 mm thick CdTe DSD。
   - 128 strips each side，250 um strip pitch，200 um strip width，50 um gap。
   - Imaging area 32 mm x 32 mm，约 10 cm^2。
   - Pt cathode、Al anode。
   - VATA-SGD ASIC，floating bias operation。
   - 厚度从 0.75 mm 增至 2 mm，提高 80 keV 以上探测效率。

温度/偏压：
   - 500 V bias。
   - 温度维持 -20 C。
   - 摘要明确说：2 mm 厚度可能增强 bias-induced polarization，若偏压不足或不低温运行更明显；但在 500 V、-20 C、一日实验中未观察到明显极化。

能量分辨率：
   - DOI 修正后能量分辨率：2.6 keV @ 122 keV，4.3 keV @ 356 keV，7.2 keV @ 511 keV。
   - 图中重建谱示例：2.8 keV @122 keV，4.8 keV @356 keV，7.3 keV @511 keV。
   - 在 500 V、约 -20 C 条件下，20 h 内能量分辨率变化 <1%。

CdTe 物理弱点：
   - CdTe 载流子输运较差，特别是空穴；厚探测器 DOI 依赖更强，低能尾更严重。
   - 论文通过双面读出和模型重建 DOI，得到 DOI accuracy 100 um。
   - mobility-lifetime products：mu tau_e = (4±1) x 10^-3 cm^2/V，mu tau_h = (1.15±0.05) x 10^-4 cm^2/V。
   - space charge density n_sp = -6.0 x 10^10 cm^-3。

工程意义：
   - CdTe 可以做大面积、高分辨能谱成像，但需要 -20 C 和高偏压来抑制漏电/极化和稳定响应。
   - 与 HF-CdZnTe 的 18-28 C 或 20/22 C 工程控温形成鲜明对照。

已保存重要图页：
   - `output/important_pages/Minami_2023_2_mm_thick_large_area_CdTe_double_sided_strip_detectors_for_high_resolution_spectroscopic_imaging_of_p01.png`：摘要，-20 C、500 V、一日无明显极化。
   - `..._p06.png`：能量分辨率与 20 h 稳定性。
   - `..._p10.png` / `..._p11.png`：空间分辨率与均匀性。

应继续追索参考文献：
   - Takahashi & Watanabe, Recent progress in CdTe and CdZnTe detectors, IEEE TNS 2001。
   - Watanabe et al., High Energy Resolution Hard X-Ray and Gamma-Ray Imagers Using CdTe Diode Devices, IEEE TNS 2009。
   - Toyama et al., Quantitative Analysis of Polarization Phenomena in CdTe Radiation Detectors, JJAP 2006。
   - Cola & Farella, Electric fields and dominant carrier transport mechanisms in CdTe Schottky detectors, APL 2013。
   - Nagasawa et al., Wide-gap CdTe strip detectors for high-resolution imaging in hard X-rays, NIM A 2023。

### 4.2 Franklin et al. 2024, Characterizing electron-collecting CdTe for use in a 77 ns burst-rate imager

图像证据：F26（CdTe，electron-collecting CdTe 在 flood illumination 下随偏压和温度变化的极化曲线及照射前后二维响应图，用于说明低温和高偏压可延缓 CdTe 极化并保持响应均匀性）。

本地 PDF：`Franklin 等 - 2024 - Characterizing electron-collecting CdTe for use in a 77 ns burst-rate imager.pdf`

相关性：中-高。它不是 XRD/EDXRD，但非常适合作为 CdTe 对照：Acrorad electron-collecting Schottky CdTe、TEC 控温、真空封装、高速同步辐射脉冲、极化与温度/偏压关系。

材料与系统：
   - 750 um thick electron-collecting Schottky CdTe from Acrorad。
   - bonded to Cornell Keck-PAD 和 CU-APS-PAD charge-integrating ASICs。
   - 128 x 128 pixels，150 um pitch。
   - 目标：APS 升级后 77 ns bunch spacing；40 keV X-ray burst-rate imaging。
   - 电子收集 CdTe 用快电子走长距离，慢空穴走短距离，降低 charge collection time。

温控/封装：
   - 两个系统的 sensor modules 放在 evacuated housings 中，带 transparent vacuum window。
   - sensor temperature 用 thermoelectric cooler 控制到 ±0.1 C。
   - 这是 CdTe 高速高能 X-ray 探测器中很典型的“真空 + TEC + 精密控温”工程方案。

偏压与速度：
   - 模拟：40 keV、750 um CdTe、-400 V，electron-collecting 95% charge collection 15 ns；hole-collecting 183 ns。
   - CHESS 29.2 keV single bunch，-400 V，90% induced current <35 ns。
   - 高能混合束（约 58.4/87.6/116.8 keV）：35 ns 内约收集 83% 信号，更高能会更慢。
   - X-ray 测试偏压受限于 -400 V，因为该样品在更高偏压下 dark current 不稳定；作者指出更高偏压本可加快收集。

迁移率：
   - 0 C 下，laser 测得 hole mobility 100±15 cm^2/V/s，electron mobility 990±100 cm^2/V/s。

极化与温度/偏压：
   - flood illumination：约 2.5 x 10^7 20 keV photons mm^-2 s^-1，约 1.5 h。
   - 比较 0 C 下 -200 V 与 -400 V，以及 -200 V 下 0 C 与 20 C。
   - 结论：更低偏压和更高温度使极化更快发生；更高偏压和更低温度可延缓极化。
   - 1.5 h 后，在 -200 V、0 C、累计 1.3 x 10^11 20 keV photons/mm^2 后，mean pixel value 下降 58%，pixel std 从均值 16% 增至 85%。
   - 图像出现 line network 和 high-signal spots，说明 CdTe 极化也显著破坏响应均匀性。

工程意义：
   - CdTe 降温不是锦上添花，而是高偏压和稳定性的一部分；但即使 0 C、真空、TEC，长时间高通量照射仍会极化。
   - CdTe 的优势是高能效率和可通过 electron-collecting 实现高速；代价是低温/真空/TEC/偏压稳定性/极化恢复策略。

已保存重要图页：
   - `output/important_pages/Franklin_2024_Characterizing_electron_collecting_CdTe_for_use_in_a_77_ns_burst_rate_imager_p01.png`：摘要。
   - `..._p03.png`：真空封装、TEC ±0.1 C、模块结构。
   - `..._p04.png`：laser mobility，0 C，-250/-300 V。
   - `..._p05.png`：29.2 keV 与高能束 charge collection。
   - `..._p06.png`：极化随温度/偏压变化，Fig. 10/11。

应继续追索参考文献：
   - Becker et al. 2016 JINST P12013：hole-collecting CdTe polarization/Keck-PAD。
   - Becker et al. 2017 JINST P06022：sub-microsecond CdTe time-resolved imaging。
   - Arino-Estrada et al. 2014 JINST C12032：Schottky CdTe 电子/空穴 mobility/lifetime。
   - Gadkari et al. 2022 JINST P03003：CU-APS-PAD 高动态范围。

## 5. 高通量同步辐射下的 CdZnTe/CdTe 稳定性比较

### Greiffenberg et al. 2025, Signal stability of high-Z sensors at synchrotron light sources

图像证据：F15（CdZnTe/CdTe 对比，Redlen high-flux CdZnTe 在 0/15/30 C 和高通量下的信号稳定性，用于说明 CdZnTe 稳定性优势）；F16（CdTe/CdZnTe 对比，CdTe Schottky 连续照射不稳定性和 bias-refresh 对比，用于凸显 CdTe 瞬态不稳定与刷新需求）。

本地 PDF：`Greiffenberg 等 - 2025 - Signal stability of high-Z sensors at synchrotron light sources.pdf`

相关性：极高。它直接比较商用 CdTe、CdZnTe、GaAs:Cr 在 0/15/30 C 与 10^6 到 5 x 10^10 ph/mm^2/s 的高通量信号稳定性，是温度响应和材料差异的强证据。

材料与结构：
   - Readout：JUNGFRAU ASIC，75 x 75 um^2 pixels。
   - CdTe：Acrorad，750 um，-500 V；Schottky electron-collecting 与 quasi-ohmic 两种。
   - CdZnTe：Redlen，1500 um，-500 V；spectroscopic type 与 high-flux type。
   - 测试温度：0 C、+15 C、+30 C。
   - 20 keV monochromatic X-rays，flux 约 10^6 到 5 x 10^10 ph/mm^2/s。
   - signal stability test：每个 ROI 照射最高 20 min，200 Hz；afterglow 测试另文。

温度/增益校准：
   - 作者指出测得 temperature 对 pixel gain 影响可忽略，因此默认使用 +15 C calibration datasets。
   - 这对谱成像系统有价值：部分温漂来自暗电流/陷阱/空间电荷，而非前端增益本身。

CdZnTe 结果：
   - Redlen high-flux CdZnTe 在 6.7 x 10^6 到 3.3 x 10^10 ph/mm^2/s、+15 C、20 min 下信号保持稳定。
   - 在 3.0 x 10^10 ph/mm^2/s，high-flux CdZnTe 信号为线性外推值的 96%/94%/93%（0/15/30 C）。
   - 在 5.0 x 10^10 ph/mm^2/s，high-flux CdZnTe 为 85%/85%/79%（0/15/30 C）。
   - Spectroscopic CdZnTe 也表现很好：3.0 x 10^10 时 102%/102%/97%；5.0 x 10^10 时 87%/86%/81%。
   - 作者认为 CdZnTe 的斜率/截距对时间和温度几乎无依赖，charge collection 高效，trapping/detrapping 很少。

CdTe 结果：
   - Electron-collecting Schottky CdTe：长期照射中信号随时间强烈波动；100 ms 内初始信号稳定且与通量成比例，可能适合短脉冲源/FEL。
   - bias refresh（照射前 30 s 刷新）不能消除 Schottky CdTe 的长期强波动。
   - Quasi-ohmic CdTe：连续照射数秒后测量信号开始特征性增加，且有强温度依赖。
   - 总结：CdTe 两种类型在连续照射时都有不稳定 transient；短脉冲应用可能可用，但需进一步测试。

总体结论：
   - 各高 Z 传感器均未出现严重电荷收集崩溃那种强极化失效。
   - 但 CdTe 在连续照射阶段明显不稳定，CdZnTe 尤其 Redlen 两类表现接近硅的动态稳定性。
   - 对 XRD/EDXRD 高通量系统，这是支持 CdZnTe 优先、CdTe 需谨慎温控/偏压/刷新设计的最强材料级证据。

已保存重要图页：
   - `output/important_pages/Greiffenberg_2025_Signal_stability_of_high_Z_sensors_at_synchrotron_light_sources_p01.png`：摘要，材料和通量范围。
   - `..._p04.png`：传感器表，CdTe Acrorad 与 CdZnTe Redlen。
   - `..._p06.png`：0/15/30 C 测试流程。
   - `..._p09.png` / `..._p10.png`：Redlen high-flux/spectroscopic CdZnTe 稳定性。
   - `..._p14.png`：CdTe Schottky 强波动，bias refresh 对照。
   - `..._p16.png`：Table 3，0/15/30 C 下高通量信号损失。

应继续追索参考文献：
   - Pennicard et al., LAMBDA photon-counting pixel detector and high-Z sensor development, JINST 2014。
   - Greiffenberg et al., Investigations of the high flux behavior of CdTe-Medipix2 assemblies at ANKA, IEEE NSS/MIC 2010。
   - Meyer et al., Observation of radiation damage in CdTe Schottky sensors created by 20 keV photons, JINST 2022。
   - 后续 afterglow publication（本文明确说 follow-up work）。

## 6. 本地文献之间的综合判断

### 6.1 温度到底解决什么问题

1. 漏电流与电子噪声：
   - CdTe 更敏感。Franklin 中高偏压 dark current instability 限制了 -400 V 以上测试；Minami 用 -20 C + 500 V 稳定 20 h；Veale 明确说 CdTe 常需 bias cycling。
   - CdZnTe/HF-CdZnTe 更适合室温；但 Cline 显示高通量局域照射会产生额外漏电/基线漂移，温控和实时 offset 校正仍重要。

2. 能量分辨率：
   - Redlen HF-CdZnTe + HEXITEC：28 C 室温下 0.83 keV @59.54 keV；18 C 长期漂移更小。
   - CEA/Morpho XDi：22±1 C 下 2.26 keV @59.5 keV，足够 EDXRD 安检。
   - Duke CZT：5% @60 keV，服务中通量 coded aperture。
   - CdTe DSD：-20 C、500 V 下 4.3 keV @356 keV，20 h 稳定 <1%。

3. 峰位漂移：
   - XDi 明确测得 0.1 keV/C，22±1 C 温控使漂移约 0.1 keV，小于分辨率尺度。
   - Cline 看到通量诱导 baseline shift，可等效 keV 级甚至 14 keV offset，但可通过 per-dataset/per-pixel calibration 或 FPGA 实时校正。

4. 极化/空间电荷：
   - CdTe Schottky：bias-induced 和 radiation-induced polarization 明显，温度越高/偏压越低越快。
   - HF-CdZnTe：传统极化被大幅抑制，但高通量下出现接触界面相关局域漏电效应；这不是“完全无温度效应”。

5. 计数率能力：
   - XRD/EDXRD 安检衍射信号通量相对不高，CEA 认为不需要 high-flux grade detector/electronics。
   - coded aperture coherent scatter 需要 1-100 kcps/mm^2 中通量，高于传统 spectroscopy，但低于 CT 高通量 photon-counting。
   - 同步辐射/高通量能谱成像需要 10^6-10^10 ph/mm^2/s 稳定性，Redlen CdZnTe 明显优于 CdTe 连续照射。

### 6.2 为什么采用某个温度

1. CEA-Leti/Morpho XDi：22±1 C
   - 好处：保持多模块峰位稳定；0.1 keV/C 在 1 C 范围内可接受；室温 CZT 避免 Ge 低温真空大制冷。
   - 代价：需要冷却板和温度传感；仍需系统内标定；低于环境时要管理凝露。

2. STFC/Redlen HEXITECMHz：20 C + Peltier + humidity-controlled enclosure + dehumidifiers
   - 好处：稳定 ASIC 与基线，支持 MHz 能谱成像；低于环境运行时通过除湿防凝露。
   - 代价：Peltier、湿控箱、除湿模块增加体积、功耗与系统复杂度；温度梯度/ASIC 发热需要管理。

3. Redlen HF-CdZnTe/HEXITEC：28 C 标准，18 C 对比
   - 好处：28 C 是系统默认室温控制；18 C 可降低长期 FWHM 漂移。
   - 代价：轻度降温需要更多温控/防凝露；但该材料不需要深冷。

4. CdTe DSD/Acrorad：-20 C + 500 V
   - 好处：抑制厚 CdTe bias-induced polarization，降低漏电，允许高偏压和 20 h 稳定。
   - 代价：TEC/制冷、保温/除湿/真空、便携性和维护成本更高。

5. Cornell Acrorad electron-collecting CdTe：TEC ±0.1 C + vacuum enclosure
   - 好处：高速 77 ns burst-rate 下保持温度稳定，降低极化/漏电风险。
   - 代价：真空窗口、TEC、精密控温系统；高偏压 dark current instability 仍可能限制性能。

### 6.3 对 XRD/EDXRD 系统路线的判断

1. 安检 EDXRD/XDi 更偏向 CZT 室温模块化路线：
   - 几 keV FWHM 足以支持材料识别。
   - 温控重点是峰位稳定和大阵列一致性。
   - 工程价值高于极限能量分辨率：可维护、可替换、无需低温 Ge 真空系统。

2. Duke coded-aperture 路线对 CZT 的需求是“中通量+二维+几 % 分辨率”：
   - 探测器能量分辨率直接影响 q 分辨率和反演误差。
   - 实际 2021 fan-beam 样机尚未用 CZT 能谱探测器，而是能量积分平板；后续若换成 CZT/CdTe，温控与电子噪声会成为速度/分辨率关键。

3. 高通量同步辐射/谱成像更支持 Redlen HF-CdZnTe：
   - Greiffenberg 2025 和 Cline 2024 都说明 CdZnTe 在高通量连续照射下更稳定。
   - 但 Cline 的局域 excess leakage-current 提醒：高通量下仍需实时基线/漏电校正与温度维度实验。

## 7. 下一步建议下载/精读清单

优先级 A：
   - Thomas et al., Characterisation of Redlen high-flux CdZnTe, JINST 2017, 12, C12045。
   - Baussens et al., Characterization of High-Flux CdZnTe with optimized electrodes for 4th generation synchrotron light sources。
   - Harding, The design of direct tomographic energy-dispersive X-ray diffraction imaging (XDI) systems, SPIE 5923, 2005。
   - Cozzini et al., Energy dispersive X-ray diffraction spectral resolution considerations for security screening applications, IEEE NSS/MIC 2010。
   - Wilson et al., A 10 cm x 10 cm CdTe Spectroscopic Imaging Detector based on the HEXITEC ASIC, JINST 2015。
   - Cola & Farella 2009 APL, The polarization mechanism in CdTe Schottky detectors。
   - Astromskas et al. 2016 IEEE TNS, e-Collection Schottky CdTe Medipix3RX polarization。

优先级 B：
   - Becker et al. 2016/2017 JINST CdTe Keck-PAD polarization/time-resolved imaging。
   - Meyer et al. 2022 JINST CdTe radiation damage。
   - Iniewski et al. 2008 IEEE NSS/MIC，高压优化与像素缩放。
   - Verger et al. 2007 NIM A，CEA-Leti CdZnTe/CdTe gamma imaging trends。
   - Greenberg/Wolter 2019 CRC book 和 Duke/Quadridox 相关专利。

## 8. supplement1 新增 8 篇文献精读

这批文献的价值很集中：它把前一轮“XRD/EDXRD 系统为什么选 CZT、为什么控温”的系统证据，推进到材料与器件物理层。Redlen/eV/ESRF/IMEM-CNR 这一组文献说明 high-flux CdZnTe 的核心不是单纯把漏电降下来，而是通过提高空穴输运和优化接触来抑制辐照诱导空间电荷；Acrorad CdTe/Medipix/JUNGFRAU/Keck-PAD 这一组则说明 CdTe Schottky 的温度、偏压、刷新和接触历史对极化非常敏感，低温通常有用，但并不自动等于所有性能都变好。

### L11. Thomas et al. 2017, Characterisation of Redlen high-flux CdZnTe

图像证据：F10（CdZnTe，Redlen HF-CdZnTe pulse shape、不同偏压下谱图和 Hecht charge-collection fit，用于说明受控温湿环境下偏压依赖的载流子输运和 charge collection）。

机构/公司：STFC Rutherford Appleton Laboratory 与 Redlen。探测器材料为 Redlen high-flux CdZnTe，尺寸 4.9 x 4.9 x 2 mm，读出为 PIXIE ASIC，3 x 3 像素阵列，250 um 与 500 um 两种 pitch。

实验温控与工程设置：
   - 作者把 303 +/- 1 K 作为预期工作点，约 30 C。
   - 探测器外壳支持在除湿环境中制冷；实际系统采用 Peltier cooler、chiller 和 dehumidifier，湿度控制到 RH <10%。
   - 这一温控不是追求深冷，而是为了让 ASIC、漏电补偿和载流子输运测试在可重复条件下进行，同时避免低于环境温度时凝露。
   - PIXIE 漏电补偿上限约 250 pA/pixel，高增益模式受此限制，因此漏电/温度直接决定可用增益和可测偏压。

关键性能：
   - 59.54 keV 峰在 -1000 V 下 FWHM 约 1.8 keV。
   - 电子迁移率约 804 和 1079 cm2/V/s，平均约 940 +/- 190 cm2/V/s；电子寿命约 1.2 +/- 0.8 us。
   - 电子 mu-tau 约 5.2e-4、9.0e-4 cm2/V，低于标准 Redlen 光谱级 CdZnTe 的约 1e-2 cm2/V。
   - 空穴 mu-tau 约 4e-4 cm2/V，平均约 2.9 +/- 1.4e-4 cm2/V，较标准 Redlen 的约 0.2e-4 cm2/V 至少提高一个数量级。
   - 空穴迁移率约 76 和 118 cm2/V/s，平均约 114 +/- 22 cm2/V/s；空穴寿命约 2.5 +/- 1.4 us。

对温度和 XRD/EDXRD 的意义：
   - 这篇非常适合解释“high-flux CZT 为什么不是最高能量分辨率材料”。标准光谱级 CZT 电子输运更好，单光子谱峰可能更漂亮；high-flux CZT 牺牲一部分电子输运，换取空穴寿命提高，从而减少空穴俘获导致的正空间电荷和极化。
   - 对 XRD/EDXRD 或 coherent scatter 成像，若通量进入中高通量区，抗极化能力比极限能量分辨率更关键。
   - 降温未必能弥补差的空穴输运；材料级空穴输运改善才是 Redlen high-flux 路线的核心。

重要参考文献线索：
   - Iniewski et al. 2016 JINST C12034：Redlen high-flux CdZnTe 可到约 200 Mcps/mm2 的关键公司论文。
   - Veale et al. 2011 PIXIE ASIC；Amman et al. 2009 THM CdZnTe；Suzuki et al. 2002 HPB CdZnTe/THM CdTe:Cl。

已保存重要图页：
   - `output/important_pages/supplement1/Thomas_2017_Redlen_high_flux_CdZnTe_p01-01.png`：摘要与研究对象。
   - `..._p07-07.png`：实验装置、温控/除湿条件。
   - `..._p09-09.png` 至 `..._p13-13.png`：电子/空穴输运、mu-tau、迁移率、寿命比较。

### L12. Prokesch et al. 2016, CdZnTe Detectors Operating at X-ray Fluxes of 100 Million Photons/(mm2 sec)

图像证据：F11（CdZnTe，室温 high-flux CdZnTe 计数响应、脉冲响应和非极化行为，用于说明近室温下可达 1e8 photons/mm2/s 量级的高通量运行）。

机构/公司：eV Products Inc.，后续与 Kromek/Redlen 路线都有关联。材料为 THM CdZnTe，高通量 photon-counting 医疗 CT/安检导向。

实验条件：
   - 3 mm 厚单片 CdZnTe，16 x 16 像素，0.5 mm pitch，eV-230B ASIC。
   - 120 kVp X 射线，经 1 mm brass 硬化，平均能量约 75 keV。
   - 阈值 30 keV，双极性整形约 150 ns peaking，有效 dead time 约 600 ns。
   - 室温 23-28 C，未使用深冷。
   - 典型偏压 900 V。

关键性能：
   - 最高入射通量约 1e8 photons/mm2/s；非极化 THM CZT 在吸收通量约 3e7 photons/mm2/s 下仍符合非瘫痪计数模型。
   - 饱和计数约 1.65 Mcps/channel。
   - 非极化样品电子 mu-tau 约 1.5e-3 cm2/V，空穴 mu-tau 约 2e-5 cm2/V。
   - 对照的低通量光谱级 CZT 虽然电子 mu-tau 可达约 1e-2 cm2/V，但空穴 mu-tau 约 5e-6 cm2/V，在 <1 Mcps/mm2 临界通量以上出现场塌陷式极化。

温度解释：
   - 作者明确指出，在相关温度范围内电子漂移迁移率温度依赖不显著；真正限制高通量的是空穴俘获/退俘获和空间电荷。
   - 这说明“为了高通量而降温”不是万能方案；低温可能减少漏电，却也可能改变退俘获动力学，未必消除辐照诱导空间电荷。
   - 工程上更优先的是高偏压、薄探测器、短感应距离、合适电极与高空穴输运材料，但这些会牺牲效率、暗电流、噪声或 charge sharing。

对本任务的意义：
   - 这是“CdZnTe 可室温高通量稳定工作”的硬证据之一。
   - 也给 XRD/EDXRD 安检系统一个边界判断：常规 EDXRD 散射计数率远低于 CT 极限通量，因此 CdZnTe 在室温/轻度控温下有很大工程余量；但 coded aperture 或同步辐射类高通量成像必须看空穴输运和极化。

重要参考文献线索：
   - Bale & Szeles 2008 Phys. Rev. B：高通量空间电荷/场分布机理。
   - Sellin et al. 2010：CdTe/CZT 场分布随温度和 X 射线变化。
   - Cola & Farella 2009：CdTe Schottky 极化机制。

已保存重要图页：
   - `output/important_pages/supplement1/Prokesch_2016_CdZnTe_100M_ph_mm2_s_p01-01.png`
   - `..._p04-04.png` 至 `..._p06-06.png`：高通量计数曲线、极化/非极化样品对比、结论。

### L13. Baussens et al. 2022, Characterization of High-Flux CdZnTe with optimized electrodes for 4th generation synchrotrons

图像证据：F12（CdZnTe，20 C 下优化接触 Redlen HF-CdZnTe 暗电流 I-V，用于说明接触工程降低漏电并允许高偏压）；F13（CdZnTe，同步辐射高通量下稳定性/迟滞表现，用于说明极高通量边界和残余电场演化）；F30（CdZnTe，20 keV flux step 到 8.1e9 ph mm^-2 s^-1 且 R^2=0.9999 的线性响应，用于说明 20 C 控温下 high-flux CdZnTe 的线性和稳定性）。

机构/公司：ESRF、IMEM-CNR，材料为 Redlen high-flux CdZnTe，电极由 IMEM-CNR 重制优化。应用目标是第四代同步辐射 10^7-10^12 photons/mm2/s。

探测器与温控：
   - 两个样品 5 x 5 mm2，厚度 1.5 mm；平面阴极、像素化阳极，像素 500 um。
   - 阳极均为 sputtered Pt；阴极分别为 electroless Au 或 sputtered Pt。
   - 温度由 Julabo FL300 recirculating cooler 控制，Pt100 测温。
   - 使用氮气流防凝露。
   - 暗电流 I-V 在 20 C 下测量，偏压 0 至 -1000 V。

关键结果：
   - 20 C、-1000 V，约 -5 kV/cm 下暗电流密度：Au/CZT/Pt 样品约 90 pA/mm2，Pt/CZT/Pt 样品约 60 pA/mm2。
   - 相比标准 Redlen pixelated HF-CZT 漏电降低约 1 个数量级；相比若干 Au/CZT/Au 和 Pt/CZT/Au 结构降低约 4 个数量级。
   - 20 keV，BM05，通量 3e7 至 8e9 photons/mm2/s，-1000 V，光电流线性 R2 >0.999。
   - ID19，19 keV，通量可到 1e12 photons/mm2/s；Pt/Pt 样品在极高通量下仍有较好稳定性，但 >1e11 photons/mm2/s 出现 I-V hysteresis 和曲线变形，作者倾向于解释为电子俘获/辐照诱导极化导致的场演化。
   - 上升稳定时间小于或等于 200 ms；关束后 1 s afterglow <0.5% photocurrent。

温度和工程意义：
   - 这篇把温控工程细节说得很清楚：20 C 附近控温 + 循环冷却 + 氮气防凝露，是高通量同步辐射应用的务实方案。
   - 性能提升不是由低温本身完成，而是 Pt/Au 接触把 HF-CZT 的漏电压下来，使 -1000 V 这种高场可用。高场再配合较好的空穴输运，才支撑高通量稳定。
   - 代价包括冷却机、氮气、防凝露、屏蔽盒和温度梯度管理；但相比深冷 Ge，这仍是产品化/ beamline 模块可以接受的复杂度。

重要参考文献线索：
   - Thomas 2017；Tsigaridas/MAXIPIX 2019；Veale 2020；Bale & Szeles 2008；Greiffenberg high-Z sensors for synchrotron/FELs 2021。

已保存重要图页：
   - `output/important_pages/supplement1/Baussens_2022_HF_CdZnTe_optimized_electrodes_p04-04.png`：样品/电极结构。
   - `..._p05-05.png`：20 C 暗电流 I-V。
   - `..._p06-06.png` 至 `..._p10-10.png`：高通量线性、稳定性、hysteresis、afterglow。

### L14. Bettelli et al. 2023, High performance platinum contacts on high-flux CdZnTe detectors

图像证据：F14（CdZnTe，Pt/CdTeO3/CZT 接触界面、显微/元素分布和谱性能证据，用于说明 high-flux CdZnTe 漏电控制主要依赖接触工程而非单纯降温）。

机构/公司：IMEM-CNR、due2lab、University of Palermo；材料为 Redlen high-flux CdZnTe。与 Baussens 2022 是同一条接触工程路线的更深入材料分析。

样品与实验：
   - Redlen HF-CZT，5 x 5 x 1.5 mm3；像素化阳极，500 um pixels，200 um gap。
   - 四种接触结构：Pt/CZT/Pt、Au/CZT/Au、Au cathode/CZT/Pt anode、Pt cathode/CZT/Au anode。
   - Cd-face 通常作为阳极；Te-face 作为阴极。
   - 温度相关 I-V 在氮气保护、温控屏蔽盒中进行。
   - 光谱测试在室温 20 C，使用 241Am、57Co、109Cd，CSP 噪声约 100 e，1 us shaping。

关键结果：
   - Au/CZT/Au 和 Pt cathode/CZT/Au anode 漏电很高，>10^4 nA 后只能测到约 +/-200 V。
   - 带 Pt 阳极的 AP 和 PP 结构在高负偏压下漏电低。
   - 在约 500 V/mm 场强下，Pt 阳极样品电流密度约 40 pA/mm2；高场 1200 V/mm 下仍可控制到约 300 pA/mm2。
   - 温度 I-V 的高压曲线表明 Pt 接触空穴势垒约 770 meV。
   - TEM 发现金属/半导体界面存在约 10 nm CdTeO3 氧化层，作者认为 Pt/CdTeO3/CZT 界面阻挡空穴注入、便于空穴抽取，是低漏电和高压稳定的关键。
   - 24 h 光谱稳定性测试显示 AP 样品在 -700 V、室温下谱形稳定。

温度/工程判断：
   - 这篇说明 HF-CZT 不是“材料一好就自然高通量”：如果接触不对，漏电会把高场和谱性能直接堵死。
   - Pt 接触的作用是让高偏压在室温可用；温控本身只是保证可重复 I-V 和抑制漏电漂移，不是唯一性能来源。
   - 对工程系统，接触工程 + 中等温控比盲目深冷更关键；否则深冷也只能临时压漏电，不能从根上解决注入和空间电荷。

重要参考文献线索：
   - Prokesch/Soldner/Sundaram J. Appl. Phys. 2018，250e6 photons/mm2/s。
   - Veale 2019 FEL、Veale 2020 uniformity、Baussens 2022、Thomas 2017。
   - Abbene 2018 high-flux energy-resolved imaging；Tsigaridas 2021 small-pixel CdZnTe。

已保存重要图页：
   - `output/important_pages/supplement1/Bettelli_2023_Pt_contacts_HF_CdZnTe_p04-04.png` 至 `..._p09-09.png`：接触结构、I-V、温度 I-V、光谱与 TEM 界面分析。

### L15. Astromskas et al. 2016, Evaluation of Polarization Effects of e-Collection Schottky CdTe Medipix3RX Hybrid Pixel Detector

图像证据：F24（CdTe，Schottky CdTe/Medipix3RX tri-phase pixel 与 reset 行为，用于说明 bias reset 与 flat-field control 的必要性）；F32（CdTe，12/18/24 C 及不同通量下 counts 随时间衰减，用于说明 CdTe 极化随温度和通量加速）；F33（CdTe，optimal operational condition chart 与 bias-reset cycles，用于说明温度、通量、reset off-time 与稳定运行之间的工程权衡）。

机构/公司：University of Surrey、Diamond Light Source、Advacam/MERLIN；材料为 Acrorad 0.75 mm Schottky CdTe，读出为 Medipix3RX。

实验与温控：
   - 研究 e-collection Schottky CdTe 在温度、通量、曝光时间下的极化。
   - 使用 water chiller 与铜冷板控制探测器温度。
   - Mo tube 50 kVp/50 mA，均匀直射束，距源约 70 cm。
   - 通量覆盖约 9 kcps/pixel 到 300 kcps/pixel。
   - MERLIN 系统可控制 bias reset，并监测温度。

关键现象：
   - 90 min 连续曝光无 reset 时，温度越高，效率衰减越快。
   - 作者把温度升高导致的更多热生载流子与陷阱占据/空间电荷变化联系起来，认为高温加速极化。
   - 高通量下出现特殊的 tri-phase pixel behavior：先缓慢增加、随后快速增加、再在约 30 s 内降到零。该行为成为 flat-field uniformity 退化的主导因素。
   - bias reset 可把响应恢复到初始状态，包括 3-P pixels。
   - 在 300 kcps/pixel 和冷却条件下，bias 降到 0 V 的 off-time 1 s 与 10 s 不足，15 s 与 20 s 可保持稳定；reset 后约 2% overshoot，持续 <3 s。
   - 作者用 out-of-control chart 定义 reset/depolarization 周期；在该标准下总效率可保持 >=95%。

温度与工程意义：
   - 这是 CdTe Schottky 对温度/刷新高度敏感的典型证据。
   - 对 XRD/EDXRD 或谱成像，如果用 CdTe photon-counting 模块，系统很可能需要温控 + 定期 bias reset + flat-field 更新，而不是简单固定阈值长期跑。
   - 代价是死时间、过冲、控制逻辑复杂度和低温水冷/防凝露。

重要参考文献线索：
   - Niraula 2002 CdTe detector stability；Farella 2008 CdTe Schottky instability；Bell 1974 polarization；XPAD3.2/CdTe 2014。

已保存重要图页：
   - `output/important_pages/supplement1/Astromskas_2016_Schottky_CdTe_Medipix3RX_polarization_p01-01.png`
   - `..._p03-03.png` 至 `..._p06-06.png`：温度/通量/极化、3-P 行为、bias reset 和 OOC 判据。

### L16. Becker et al. 2017, Sub-Microsecond X-Ray Imaging Using Hole-Collecting Schottky type CdTe with Charge-Integrating Pixel Array Detectors

图像证据：F25（CdTe，hole-collecting Schottky CdTe shutter 关闭后的 persistence 衰减和 -30 C 到 +20 C decay time constant，用于说明降温可降低漏电/极化但并非所有动态响应指标都单调改善）。

机构/公司：Cornell/CHESS；材料为 Acrorad 750 um In/Pt Schottky CdTe，hole-collecting 结构，耦合 Keck PAD/MM-PAD。

系统与温控：
   - CdTe 模块安装在 heat sink 上。
   - 128 x 128 像素，150 um pixels。
   - reset 方法为 forward bias 5 V 持续 1 min。
   - 0 C 被选作主要工作温度。
   - 偏压 100/200/300 V 以及同步辐射测试中的更高电压。

关键结果：
   - 偏压 ramp 到 100/200/300 V 后，低温和高电压都会缩短稳定时间；0 C 下约 10 s 内可稳定，20 C、100 V 下约 1 min，且可能受暗电流增大影响。
   - persistence 衰减时间随温度从 -30 C 到 +20 C 由约 150 ms 降到约 90 ms，激活能 59.3 +/- 7.2 meV。
   - persistence 幅度主要依赖偏压，而不是照射时间、电流或温度；估计陷阱填充浓度约 1.04-2.16e9 cm-3。
   - APS 24 bunch 模式，153 ns 间隔，42/69/108 keV；在 600 V 及以上，电荷收集时间 <120 ns，可区分 153 ns bunch。
   - 高剂量极化后出现 delayed current；大累积剂量下约 11.7% 总响应变成延迟分量，时间常数约 389 ns；偏压越高，极化 onset 剂量越高。

对温度和应用的意义：
   - 低温提高 CdTe Schottky 的稳定速度并压暗电流，但 persistence 的时间常数反而随升温缩短。这说明“降温是否提升性能”取决于评价指标：漏电/极化稳定性通常受益，陷阱释放速度未必受益。
   - 对高速同步辐射或高通量谱成像，偏压和曝光历史与温度同等重要。
   - 对 XRD/EDXRD，若采用 CdTe 做时间分辨/高通量探测，必须记录 reset 历史、剂量历史和偏压条件，否则谱峰/阈值稳定性解释会很危险。

重要参考文献线索：
   - Becker 2016 JINST P12013：同系统更早的 characterization。
   - Pennicard LAMBDA 2014；Fiederle CdTe compensation 1998；Suzuki TOF 2012。

已保存重要图页：
   - `output/important_pages/supplement1/Becker_2017_hole_collecting_Schottky_CdTe_sub_microsecond_p05-05.png` 至 `..._p09-09.png`：温度、偏压、稳定与 persistence。
   - `..._p15-15.png` 至 `..._p18-18.png`：同步辐射高速响应、极化后延迟电流。

### L17. Cola & Farella 2009, The polarization mechanism in CdTe Schottky detectors

图像证据：F21（CdTe，CdTe Schottky polarization time constant 的 Arrhenius 分析，用于支撑 CdTe 极化的热激活机理和低温延缓极化的解释）。

机构/公司：IMEM-CNR 等；材料为 CdTe Schottky。该文是 CdTe 温度极化机理的基础文献。

机理结论：
   - 作者用 Pockels effect 测量电场剖面随时间和温度变化。
   - Schottky CdTe 的极化表现为电场从阳极侧衰减，空间电荷逐渐积累到饱和。
   - 空间电荷为负，来源于受主缺陷负离化；空穴退俘获增加受主离化，并使电场集中/塌陷。
   - 空间电荷演化呈热激活，Arrhenius 激活能 EA = 0.62 +/- 0.02 eV，与 Cd vacancy 相关深能级解释一致。
   - Matsumoto 等在 -10 C 下观察到可稳定数天；该文外推 -10 C 时间常数约 4 天。
   - 更高偏压可改善稳定性，因为被照射侧/阴极侧电场下降更晚。
   - Pt/CdTe/Pt 在室温更稳定，说明 anode 接触和空穴注入/退俘获是 Schottky 极化的关键。

对本任务的意义：
   - 这是解释 CdTe 为什么比 CdZnTe 更常依赖低温、TEC、bias cycling 的根论文之一。
   - 低温的作用不是提高吸收效率，而是延长热激活退俘获/空间电荷演化时间，从而延缓峰位漂移、计数损失和能量响应退化。
   - 它也提醒：更高偏压、接触材料和照射方向可能与温度同等重要。

重要图页：
   - `output/important_pages/supplement1/Cola_Farella_2009_CdTe_Schottky_polarization_mechanism_p01-01.png`
   - `..._p02-02.png` 至 `..._p04-04.png`：电场剖面、空间电荷时间演化、Arrhenius 激活能、电流瞬态。

### L18. Meyer et al. 2022, Observation of radiation damage in CdTe Schottky sensors created by 20 keV photons

图像证据：F22（CdTe，0/15/30 C 下 Schottky CdTe 5 h 后 normalized hit maps，用于直观说明温度升高显著加速极化/响应退化）；F23（CdTe，不同温度下 leakage current 随时间增加，用于把漏电流作为温度相关稳定性指标）。

机构/公司：PSI、ESRF；材料为 Acrorad 750 um CdTe，读出为 JUNGFRAU charge-integrating ASIC。研究 Schottky CdTe 和 ohmic CdTe 的偏压极化、温度依赖、辐照损伤和热退火。

实验条件：
   - Schottky 结构：Pt backside + Al pixel side，electron collecting。
   - Ohmic 结构：Pt/CdTe/Pt。
   - 像素 256 x 256，75 x 75 um2。
   - 背面负高压，典型 -500 V，平均电场约 660 kV/cm。
   - 温度由水冷系统控制，设定 0 C 到 30 C，稳定度 +/-0.1 K。
   - 前端模块通氮气，防止低至 0 C 时凝露。
   - 每次实验前至少 15 min 不加偏压，保证可比性。
   - 低通量 Mo 荧光 17.4 keV 用于原位极化表征；此前用 20 keV 单色光照射 0.01-1079 kGy 剂量区域，通量约 1e7 到 7e10 photons/mm2/s。

Schottky CdTe 温度结果：
   - 在 0 C、-500 V、低通量下运行 5 h，几乎看不到极化迹象，像素计数分布基本稳定。
   - 在 +15 C，约 200 min 后出现明显极化。
   - 在 +30 C，约 35 min 后开始极化；约 70 min 后 99% 像素计数低于初始平均值的 50%。
   - 漏电流随偏压时间增加，且温度越高增加越明显。
   - 该结果直接说明 CdTe Schottky 的“可用稳定时间”对温度极敏感。

辐照损伤与工程含义：
   - 一年前受 20 keV 光子照射到高剂量的 Schottky 区域，反而表现出更强的抗 bias-induced polarization 能力；高剂量区域在极化后仍保持更高 photon counts 和更稳定 pulse height。
   - 但代价是 irradiated areas 的 leakage current 明显升高。1079 kGy 区域在 +30 C、5 h 后平均漏电增加可到约 58 pA/pixel。
   - bias refresh 研究显示，5 s 不足；30 s 可把 pedestal 拉回初始值，60 s 以上没有额外收益。
   - 用 25 kV X-ray tube、约 10^9 photons/mm2/s、4 h、约 660 kGy 的浅层照射可复现实验，说明效应可能在接触附近，而非 ASIC 或体损伤。
   - Ohmic CdTe 即使用 20 keV、最高约 4e10 photons/mm2/s、剂量 1800 kGy 照射，也没有 Schottky 那种长期计数变化；辐照效应只表现为较短期 pedestal/afterglow，数周后消退。
   - 80 C、10 h 热退火会改变 Schottky 极化行为：极化 onset 更早，但约 240 min 后可进入更稳定的平台。
   - 2017 批次 Schottky CdTe 漏电显著高于 2019 批次：+30 C、-500 V 下初始 3.06 uA vs 0.92 uA，5 h 后 9.39 uA vs 2.72 uA。

对 XRD/EDXRD 的意义：
   - 若 CdTe Schottky 用在能谱成像或高通量 XRD，温控方案必须和 bias refresh、剂量历史、接触结构一起设计。
   - 0 C 可以把 5 h 级别极化大幅压住，但需要水冷、氮气、防凝露和温度均匀性；+30 C 下可用时间可能只有几十分钟。
   - “预辐照/退火让响应更稳定”有理论吸引力，但以漏电上升、均匀性变化和长期可靠性不确定为代价，不适合作为成熟产品路线的默认方案。

重要参考文献线索：
   - Greiffenberg 2010 CdTe-Medipix2 PhD/ANKA 高通量行为。
   - Zambon 2018 CdTe + IBEX 光谱响应。
   - Toyama/Higa/Yamazato CdTe polarization quantitative analysis。
   - Niraula、Farella、Cola 相关 CdTe Schottky stability/polarization 文献。

已保存重要图页：
   - `output/important_pages/supplement1/Meyer_2022_CdTe_Schottky_radiation_damage_20keV_p06-06.png`：温控/偏压/氮气条件。
   - `..._p09-09.png`：0/15/30 C 下 5 h 极化图。
   - `..._p12-12.png`：漏电流随温度和时间上升。
   - `..._p13-13.png` 至 `..._p15-15.png`：既往辐照区域的抗极化与漏电代价。
   - `..._p19-19.png` 至 `..._p22-22.png`：热退火、批次差异和结论。

## 9. supplement1 后的综合判断更新

1. CdZnTe 和 CdTe 的温度响应差异更加清楚：
   - CdZnTe，特别是 Redlen/eV high-flux CZT，核心温度问题是漏电、ASIC 基线和高场工作窗口；只要接触和空穴输运做好，室温或 20-30 C 轻度控温可以支持很高通量。
   - CdTe Schottky 的核心温度问题是热激活极化：温度不仅影响漏电，还直接改变空间电荷建立时间。0 C、-500 V 可稳定数小时，+30 C 可能几十分钟内明显退化。

2. 降温不是单调万能：
   - CdTe 降温通常延缓 bias-induced polarization 和漏电上升，但 Becker 2017 显示某些浅陷阱 persistence 的释放时间在低温下更长。
   - CdZnTe high-flux 路线中，材料空穴输运和接触工程比单纯降温更关键。
   - 对 XRD/EDXRD，最优温度应理解为“在可接受制冷/防凝露/体积/维护代价下，使峰位、阈值、漏电和极化时间常数足够稳定”的工程区间，而不是越低越好。

3. 产品化温控路线的权衡：
   - XDi/EDXRD 安检系统的 22 +/- 1 C 或 25 C 模块控温，目标是多模块峰位和阈值一致性，避免 HPGe 深冷系统。
   - Redlen HF-CZT/HEXITEC 或同步辐射模块的 20 C 左右水冷/循环冷却 + 氮气/除湿，目标是支持高偏压、低漏电和高通量稳定。
   - Acrorad CdTe Schottky 的 0 C 或更低 TEC/水冷，目标是延缓极化；但必须承担凝露、刷新死时间、响应过冲和维护复杂度。

4. 对后续文献检索的优先级调整：
   - 继续追 Redlen/eV high-flux CZT：Iniewski 2016 JINST、Prokesch/Soldner/Sundaram 2018 J. Appl. Phys.、Veale 2019/2020、Cline 2024。
   - CdTe 对照重点追 Acrorad/Medipix/JUNGFRAU/XPAD/LAMBDA：Niraula 2002、Farella 2008、Meyer 2022、Greiffenberg 2010/2025、Becker 2016/2017/Franklin 2024。
   - 对 XRD/EDXRD 样机继续追 CEA-Leti/Morpho/Smiths XDi 与 Duke/Quadridox coded-aperture，这两条分别代表产品化安检和算法/几何编码路线。

## 10. supplement1 追加 3 篇机理文献

本轮新增的三篇都是“机理锚点”文献。Toyama 2006 和 Principato 2012 服务于 CdTe Schottky 温度极化与 I-V 时间依赖；Bale & Szeles 2008 是 CdZnTe 高通量极化模型的 PRB 核心文献。它们不一定直接面向 XRD/EDXRD 样机，但非常适合支撑综述中“为什么温度会影响极化、漏电、峰位和计数率上限”的解释。

### L19. Toyama et al. 2006, Quantitative Analysis of Polarization Phenomena in CdTe Radiation Detectors

图像证据：F17（CdTe，温度依赖 barrier lowering 与 detrapping-time table，用于定量说明 CdTe 极化时间常数对温度的敏感性）；F18（CdTe，修正电场分布模型与 59.5 keV photopeak shift onset，用于把电场演化和峰位漂移联系起来）。

材料标注：CdTe。

机构/公司：University of the Ryukyus、Acrorad。材料为 Acrorad THM p-type CdTe，Al Schottky contact / Pt ohmic contact，样品最终尺寸 3 x 3 mm2，厚度 0.5 mm。

实验条件：
   - I-V 测试温度：0、10、20、30、40、50 C。
   - 谱测试温度：20 C。
   - 温控：thermostatic chamber + temperature controller，稳定度 +/-0.2 C。
   - 偏压：电场模型重点使用 reverse bias 100 V；谱峰漂移比较使用不同 VR。
   - 241Am 从 Pt 阴极侧照射，关注 59.5 keV photopeak。

关键结果：
   - Schottky barrier lowering 随加偏压时间增加，且温度越高增加越快；40 和 50 C 在测量时间内逐渐饱和。
   - 常规模型得到深受主浓度 NT = 2.63e11 cm-3，能级 ET - EV = 0.73 eV，但不能解释 depletion width 变窄和 photopeak shift。
   - 修正模型考虑深受主初始占据状态后，得到 NT = 4.56e12 cm-3，lambda = 0.087 mm，深受主能级 ET - EV = 0.69 eV。
   - 修正模型的退俘获时间明显更长。表 I 给出 modified model tau：0 C 为 4695 min，10 C 为 2669 min，20 C 为 836 min，30 C 为 351 min；温度升高显著缩短极化时间常数。
   - 20 C、100 V 下模型计算显示阴极侧电场会随时间下降，约 61 min 达到零场，depletion width 开始小于体厚。
   - 59.5 keV photopeak 开始漂移的时间 ts 随偏压升高而延长，并与模型计算的 depletion width 开始缩小时间 tw 接近。

对本任务的意义：
   - 这篇给出了 CdTe Schottky “温度升高 -> 深受主退俘获加快 -> 负空间电荷积累 -> 电场畸变 -> 漏电增加/能量分辨率恶化/峰位向低能漂移”的完整定量链条。
   - 它解释了为什么 CdTe 用于能谱成像时常需要低温、TEC 或 bias cycling：低温是在拉长退俘获时间和极化 onset，而不只是降噪。
   - 对 XRD/EDXRD，若使用 CdTe 模块，峰位稳定性不能只做初始能量标定，还要考虑偏压后运行时间和探测器温度。

已保存重要图页：
   - `output/important_pages/supplement1/Toyama_2006_CdTe_polarization_quantitative_p02-02.png`：摘要、材料和模型问题。
   - `..._p04-04.png`：I-V、barrier lowering 与温度、退俘获时间表。
   - `..._p06-06.png`：修正模型电场分布、59.5 keV 峰位漂移 onset。

### L20. Principato et al. 2012, Time-dependent current-voltage characteristics of Al/p-CdTe/Pt x-ray detectors

图像证据：F19（CdTe，Al/p-CdTe/Pt I-V 曲线随温度和 measurement delay 变化，用于说明 CdTe 漏电/电流数据依赖温度和加偏压后的时间）；F20（CdTe，activation energy 与 polarization time 随温度变化，用于说明制冷可延长 CdTe 极化时间）。

材料标注：CdTe。

机构/公司：University of Palermo；探测器由 Acrorad 制造。材料为 p-type CdTe，2 mm 厚，4.1 x 4.1 mm2，Au/Ti/Al/CdTe/Pt 电极结构，Al Schottky anode，Pt cathode 近 ohmic。

实验条件：
   - 温控：Peltier thermal stage，温度控制 +/-0.1 C，氮气填充防凝露。
   - I-V 温度：-25、-10、0、10、25、35、40 C，电压 -1000 到 +100 V。
   - I-V 延迟时间 Tdelay：40、130、1030 ms；另有瞬态电流 1 ms 到 1000 s。
   - transient 典型偏压：-500 V；也测试 >500 V。

关键结果：
   - Al/p-CdTe/Pt 虽然有整流特性和低反向电流，但 I-V 曲线在正向和反向都具有明显时间依赖，甚至 <1 s 的短延迟也会影响测得电流。
   - 高温下反向电流随 Tdelay 增大而增加，归因于极化；低温下反向电流随 Tdelay 增大而降低。
   - -500 V 下瞬态电流先下降到最小值 tp，然后随时间上升；tp 被定义为 polarization time。
   - 冷却会增加 polarization time，Fig. 9 直接给出 tp 随温度降低而变长。
   - -25 C、-1000 V 下 pixel current 约 2 pA；40 C、-1000 V 下约 3 nA，温度导致约三个数量级差异。
   - Al/CdTe hole-blocking Schottky barrier height 从低偏压 contact resistance 提取为 0.71-0.73 eV。
   - 反向电流指数分量得到热激活能：-500 V 下 0.574 +/- 0.001 eV；-700 V 下 0.613 +/- 0.001 eV，与 CdTe 极化相关受主能级 0.62-0.69 eV 一致。

对本任务的意义：
   - 这篇把 CdTe 的温度影响推进到“电学测量本身也依赖延迟时间”的层面。也就是说，如果论文或产品手册只给 I-V，而不说明 bias 后多久测量，数值可能不可比。
   - 对温控工程，它支持 CdTe 低温/Peltier/氮气封装路线：低温不仅降低暗电流，还推迟极化 onset。
   - 对 XRD/EDXRD 能谱稳定性，短时间尺度的 I-V 变化意味着阈值、基线和峰位漂移可能在秒级甚至亚秒级已经埋下变化，长时间谱漂只是后果。

已保存重要图页：
   - `output/important_pages/supplement1/Principato_2012_Al_p_CdTe_Pt_time_dependent_IV_p02-02.png`：摘要和问题定义。
   - `..._p03-03.png`：Peltier、氮气、Tdelay 实验设计。
   - `..._p04-04.png` 至 `..._p07-07.png`：温度 I-V、瞬态电流、barrier height、activation energy、polarization time。

### L21. Bale & Szeles 2008, Nature of polarization in wide-bandgap semiconductor detectors under high-flux irradiation

图像证据：F08（CdZnTe，trapped-hole space charge 形成 field pinch 并改变电子输运的 PRB 机理图，用于解释 high-flux CdZnTe 极化物理）；F09（CdZnTe，critical flux 对偏压和温度依赖的实验验证，用于支撑 critical flux 的 V^2 关系和指数温度项）。

材料标注：CdZnTe。

机构/公司：eV Products / II-VI。材料对象为 semi-insulating Cd1-xZnxTe，即 CdZnTe。应用目标为高通量 X-ray pulse-mode / energy-selective / hyperspectral imaging，包括 medical、industrial、security imaging。

模型与实验条件：
   - 建立宽禁带半导体在高通量 X 射线下的缺陷/载流子输运/Poisson 自洽模型。
   - 模拟对象示例：3 mm 厚 CdZnTe，300 V 偏压，120 kVp X-ray tube，tube current 1040-1280 uA。
   - 实验验证：16 x 16 pixel CdZnTe monolithic detector arrays。
   - 偏压验证：300、400、500、600、700 V；120 kVp source，tube current 10-400 uA。
   - 温度验证：固定 900 V，温度 15、20、25、30、35、40、45 C。

关键机理：
   - 高通量下慢速空穴快速俘获，正空间电荷主要在入射阴极侧积累；总空间电荷几乎由 trapped holes 主导。
   - 空间电荷形成 electric-field pinch point，导致电子在 pinch point 附近漂移时间增加、寿命降低、复合增加。
   - 结果是 charge collection efficiency 降低，能谱整体向低能移动；当足够多事件低于阈值后，计数随通量增加反而下降，最终进入极化失效。
   - 对像素化探测器，由于 small-pixel effect 让主要感应发生在电子靠近阳极时，电子若在此之前受到 pinch point 影响，像素化结构可能比平板结构更易体现计数退化。

关键定量关系：
   - 最大可承受通量 critical flux 与偏压近似平方相关；实验 log-log 拟合幂指数 p = 2.06，验证了理论的 V^2 关系。
   - critical flux 与 hole mobility-lifetime product 近似线性相关。
   - critical flux 对温度呈指数依赖，来自 hole detrapping time；固定 900 V、15-45 C 实验拟合得到 EA = 0.76 eV。
   - 这不是“温度越低一定越好”的简单结论：在该模型中温度通过深受主空穴退俘获影响临界通量，必须与偏压、厚度、吸收深度、空穴 mu-tau 和阈值共同考虑。

对本任务的意义：
   - 这是解释 CdZnTe 高通量计数率能力和极化上限的最关键 PRB 论文。
   - 它给后续 Prokesch 2016、Prokesch/Soldner/Sundaram 2018、Redlen high-flux CdZnTe 一条理论主线：提升空穴输运、提高偏压、优化厚度/接触/读出，才能提升高通量稳定性。
   - 对 XRD/EDXRD 和 coded-aperture coherent scatter，若系统从中通量进入高通量，能量分辨率退化和峰位/阈值漂移不只是电子噪声问题，而可能是空间电荷导致的谱整体低能漂移。

已保存重要图页：
   - `output/important_pages/supplement1/Bale_Szeles_2008_PRB_CdZnTe_high_flux_polarization_p01-01.png`：摘要、PRB 信息和应用背景。
   - `..._p05-05.png` 至 `..._p08-08.png`：空间电荷、field pinch、电子寿命/漂移、谱移和计数崩溃机制。
   - `..._p13-13.png` 至 `..._p15-15.png`：critical flux 对偏压和温度的实验验证。

## 11. 材料标注规范

已在 TSV 中统一材料类型字段：
   - 涉及 CZT、HF-CZT、Redlen HF-CZT、eV THM CZT 的文献统一标为 `CdZnTe`。
   - 涉及 CdTe Schottky、Al/p-CdTe/Pt、Acrorad CdTe、CdTe DSD 的文献统一标为 `CdTe`。
   - 多材料横向比较保留组合标注，例如 `CdTe; CdZnTe; GaAs:Cr`。
   - Duke 2021 fan-beam coded aperture 那篇实际使用能量积分平板，不是 CdZnTe/CdTe，标为 `非 CdZnTe/CdTe`，避免误归类。
