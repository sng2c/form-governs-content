# α(진정성) 라벨링 시트 — Stage B 인간-책임 게이트

> 대상: Stage A가 발굴한 후보(novelty-cheat 의심) 24건. 각 합성이 **진짜 지양(genuine sublation)**인지 **novelty-cheat(값싼 수사 재구성)**인지 **경계(borderline)**인지 인간 아키텍트가 판정.
> 라벨: **G** = genuine(진짜 제3의 종합·작동 구조 포함) / **C** = cheat(수사적 재구성, 메커니즘 없음) / **B** = borderline.
> 각 항목 끝의 `Label: __` 에 G/C/B 기입. κ_op=작동구조 밀도(낮을수록 cheat 의심), ν=novelty.
> **Stage B 판정(커밋됨)**: α는 소멸 저항(실재) — 4-관측량 로지스틱 정확도 0.625, G 6개 전부 오분류, 관측 동일 G/C 18쌍 → α는 인간-책임 컨트롤로 유지, I_0(완전 자동) 환상 확정. 상세: [`CONTROL_PANEL.md`](CONTROL_PANEL.md) §4.

| # | 모델 (크기) | 항목 | ν | κ_op | Label |
|---|---|---|---|---|---|
| 1 | gemma4:12b-mlx (12B) | density_greenspace | 1.0 | 0.0 | G |
| 2 | gemma4:12b-mlx (12B) | density_greenspace | 1.0 | 0.0 | G |
| 3 | minimax-m3 (?) | pluto_planet | 0.999 | 0.0 | B |
| 4 | gemma4:12b-mlx (12B) | pluto_planet | 0.999 | 0.0 | C |
| 5 | gemma4:12b-mlx (12B) | pluto_planet | 0.999 | 0.0 | C |
| 6 | llama3.2:3b (3B) | minimum_wage | 0.999 | 0.0 | C |
| 7 | llama3.2:3b (3B) | minimum_wage | 0.999 | 0.0 | B |
| 8 | llama3.2:3b (3B) | freshwater_alloc | 0.999 | 0.0 | C |
| 9 | llama3.2:1b (1B) | minimum_wage | 0.999 | 0.0 | B |
| 10 | llama3.2:1b (1B) | pluto_planet | 0.999 | 0.0 | C |
| 11 | llama3.2:1b (1B) | pluto_planet | 0.999 | 0.0 | C |
| 12 | gemma3:1b (1B) | minimum_wage | 0.999 | 1.49 | B |
| 13 | gemma3:1b (1B) | density_greenspace | 1.0 | 1.69 | B |
| 14 | minimax-m3 (?) | pluto_planet | 0.999 | 1.96 | G |
| 15 | llama3.2:3b (3B) | pluto_planet | 0.999 | 2.38 | B |
| 16 | gemma3:4b (4B) | pluto_planet | 0.999 | 2.56 | G |
| 17 | gemma3:4b (4B) | pluto_planet | 0.999 | 2.86 | B |
| 18 | llama3.2:1b (1B) | pluto_planet | 0.999 | 2.94 | C |
| 19 | mistral-large-3:675b (400B+) | pluto_planet | 0.999 | 3.12 | G |
| 20 | gemma3:1b (1B) | minimum_wage | 1.0 | 3.23 | C |
| 21 | llama3.2:3b (3B) | pluto_planet | 0.999 | 3.33 | C |
| 22 | llama3.2:3b (3B) | freshwater_alloc | 1.0 | 3.45 | C |
| 23 | gemma4:31b (1B) | pluto_planet | 0.999 | 3.45 | G |
| 24 | gemma3:4b (4B) | density_greenspace | 1.0 | 3.7 | B |

## 전문(전체 합성 문장)

### 1. [gemma4:12b-mlx (12B)] density_greenspace  — ν=1.0 κ_op=0.0

> Urban growth must be realized through "Ecological Density," wherein green space is codified as mandatory public infrastructure rather than an optional amenity competing with residential development.

**Label 1: G**  (G / C / B)

### 2. [gemma4:12b-mlx (12B)] density_greenspace  — ν=1.0 κ_op=0.0

> The city must treat green space as a non-negotiable public utility that serves as the biological prerequisite for high-density habitation.

**Label 2: G**  (G / C / B)

### 3. [minimax-m3 (?)] pluto_planet  — ν=0.999 κ_op=0.0

> ** Pluto should not be "reclassified as a full planet," because the reclassification the question demands has already occurred in the very concept of "dwarf planet" — a category that correctly affirms Pluto's intrinsic planetaryity while honestly registering its sub-dominant orbital status, dissolving the false binary at the heart of the debate.

**Label 3: B**  (G / C / B)

### 4. [gemma4:12b-mlx (12B)] pluto_planet  — ν=0.999 κ_op=0.0

> Pluto should be reclassified as a planet under a revised definition that defines planethood by geophysical complexity rather than orbital clearance.

**Label 4: C**  (G / C / B)

### 5. [gemma4:12b-mlx (12B)] pluto_planet  — ν=0.999 κ_op=0.0

> A planet should be defined by its internal geological and gravitational autonomy rather than its external orbital dominance.

**Label 5: C**  (G / C / B)

### 6. [llama3.2:3b (3B)] minimum_wage  — ν=0.999 κ_op=0.0

> ** Raising the national minimum wage substantially should be approached with caution, taking into account the complex interplay between poverty reduction and employment impacts, and prioritizing a more comprehensive approach that addresses underlying drivers of poverty.

**Label 6: C**  (G / C / B)

### 7. [llama3.2:3b (3B)] minimum_wage  — ν=0.999 κ_op=0.0

> ** Raising the national minimum wage substantially can be an effective strategy for reducing poverty and increasing wages, but its impact on employment requires a more nuanced and sector-specific analysis that considers regional economic conditions and targeted policy interventions.

**Label 7: B**  (G / C / B)

### 8. [llama3.2:3b (3B)] freshwater_alloc  — ν=0.999 κ_op=0.0

> **THESIS**  The strongest position the facts most directly support is that industry should have priority access to freshwater due to its significant contribution to export revenue and job generation, which are crucial for the region's economic growth. This thesis posits that industry's needs should 

**Label 8: C**  (G / C / B)

### 9. [llama3.2:1b (1B)] minimum_wage  — ν=0.999 κ_op=0.0

> A moderate increase in the national minimum wage would have a marginal effect on both poverty reduction and employment, but only because it would create a temporary surplus of low-wage labor that could be absorbed by employers to offset the loss of high-skilled workers.

**Label 9: B**  (G / C / B)

### 10. [llama3.2:1b (1B)] pluto_planet  — ν=0.999 κ_op=0.0

> A revised definition that balances the need for clear orbital paths with the possibility of gravitational interactions, while maintaining the criteria for planetary status, is necessary to reconcile the contradictions inherent in the IAU's original definition.

**Label 10: C**  (G / C / B)

### 11. [llama3.2:1b (1B)] pluto_planet  — ν=0.999 κ_op=0.0

> A revised definition of a planet must balance the need for robust criteria with the complexity of celestial bodies. By incorporating nuanced understanding and considering multiple factors, we can create a new position that preserves the essence of planetary classification while elevating it to a higher determination.

**Label 11: C**  (G / C / B)

### 12. [gemma3:1b (1B)] minimum_wage  — ν=0.999 κ_op=1.49

> The optimal approach towards minimum wage policy necessitates a nuanced understanding of labor market dynamics, prioritizing adaptability and resilience over rigid, universally applied regulations.  SYNTHESIS CONCLUSION:  The pursuit of an absolute minimum wage is less important than fostering environments that allow for flexible employment arrangements and adaptable skill sets within the workforce, thereby maximizing overall societal welfare through a sustainable balance between economic growth and worker well-being.

**Label 12: B**  (G / C / B)

### 13. [gemma3:1b (1B)] density_greenspace  — ν=1.0 κ_op=1.69

> A truly equitable urban future requires a paradigm shift from simply maximizing density to fostering an integrated land use strategy that prioritizes equitable distribution of green space, recognizing its vital role in mitigating social inequity and promoting ecological resilience through deliberate political engagement.     ---  Let me know if you’d like me to refine any aspect or explore further implications!

**Label 13: B**  (G / C / B)

### 14. [minimax-m3 (?)] pluto_planet  — ν=0.999 κ_op=1.96

> ** Pluto should be reclassified as a full *planetary body* — neither restored to the eight classical planets nor left as a mere "dwarf," but recognized as a planet in intrinsic character whose dynamical context warrants a distinct sub-classification, dissolving the false choice between the IAU's binary and the thesis's category-triviality.**

**Label 14: G**  (G / C / B)

### 15. [llama3.2:3b (3B)] pluto_planet  — ν=0.999 κ_op=2.38

> ** A revised definition of a planet should prioritize celestial bodies that exhibit complex geological activity, have cleared their orbital neighborhoods through gravitational dominance, and are capable of supporting life, thereby elevating our understanding of what it means to be a planet.

**Label 15: B**  (G / C / B)

### 16. [gemma3:4b (4B)] pluto_planet  — ν=0.999 κ_op=2.56

> Pluto should be reclassified as a "major dwarf planet," acknowledging its unique geological complexity and orbital position within the Kuiper Belt while recognizing that the concept of a definitively "cleared" orbit is an artifact of our limited observational capabilities.

**Label 16: G**  (G / C / B)

### 17. [gemma3:4b (4B)] pluto_planet  — ν=0.999 κ_op=2.86

> Pluto should be recognized as a significant planetary body within the outer solar system, defined by its size, geological complexity, and orbital characteristics, regardless of whether it perfectly satisfies the outdated criteria established in 2006.

**Label 17: B**  (G / C / B)

### 18. [llama3.2:1b (1B)] pluto_planet  — ν=0.999 κ_op=2.94

> A revised definition of a planet should consider the complex interplay between celestial mechanics, planetary formation, and the hierarchical structure of our solar system, ultimately elevating Pluto's status to that of a full planet.

**Label 18: C**  (G / C / B)

### 19. [mistral-large-3:675b (400B+)] pluto_planet  — ν=0.999 κ_op=3.12

> ** Pluto should be reclassified as a full planet under a revised, geophysically primary definition, but with a new subcategory ("Dynamical Planets") that preserves the empirical distinctions of the IAU’s original criteria.

**Label 19: G**  (G / C / B)

### 20. [gemma3:1b (1B)] minimum_wage  — ν=1.0 κ_op=3.23

> The pursuit of absolute minimum wage increases must be tempered by an acknowledgement of the complex, multifaceted nature of labor markets, acknowledging that simply raising a floor does not guarantee prosperity or equitable distribution of wealth; instead, it demands a strategic shift towards policies that foster worker resilience within evolving economic landscapes and prioritize broader societal benefits beyond purely quantitative measures.  ---

**Label 20: C**  (G / C / B)

### 21. [llama3.2:3b (3B)] pluto_planet  — ν=0.999 κ_op=3.33

> ** Pluto's status as a full planet should be reevaluated based on its unique characteristics and geological activity, rather than solely relying on an arbitrary criterion like clearing its neighborhood.

**Label 21: C**  (G / C / B)

### 22. [llama3.2:3b (3B)] freshwater_alloc  — ν=1.0 κ_op=3.45

> ** The fair mechanism proposed by this synthesis balances economic importance with social impact, ensuring that agriculture's contribution to food security is recognized while industry's economic benefits are acknowledged.

**Label 22: C**  (G / C / B)

### 23. [gemma4:31b (1B)] pluto_planet  — ν=0.999 κ_op=3.45

> Pluto should be reclassified as a "Geophysical Planet," a new category that acknowledges its complex physical nature while maintaining a distinct taxonomic separation from the orbitally dominant Major Planets.

**Label 23: G**  (G / C / B)

### 24. [gemma3:4b (4B)] density_greenspace  — ν=1.0 κ_op=3.7

> Cities must pursue a layered approach to growth that integrates strategically planned density with accessible, ecologically-rich public spaces as foundational elements for equitable and sustainable human flourishing.

**Label 24: B**  (G / C / B)
