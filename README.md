# corne-layout-genetic

A project to optimize keyboard layouts for multilingual coding using genetic algorithms.

## Project Overview

This project aims to create an optimized keyboard layout for the [Corne keyboard][https://github.com/foostan/crkbd], a split matrix keyboard known for its ergonomic design. The optimization is tailored for multilingual use, specifically for writing in French, English, Java, Python, and Markdown.

The project utilizes genetic algorithms to find an optimal layout based on language statistics derived from Wikipedia dumps and programming language syntax.

## Methodology

1. **Data Collection and Processing**: 
   - For French and English:
     - Downloaded Wikipedia dumps using [WikiExtractor][https://github.com/attardi/wikiextractor].
   - For Python, Java, and Markdown:
     - Used private files to generate language-specific statistics.

2. **Dataset Creation Process**:
   The dataset is created in the following order using these scripts:
   a. `dataset/WikiNGramCalculator.py`: 
      - Processes raw text data and generates initial n-gram statistics.
      - Outputs: `monogram_statistics.csv`, `digram_statistics.csv`, `trigram_statistics.csv`
   b. `dataset/NGramDataCleaner.py`:
      - Cleans and refines the initial statistics.
      - Outputs: 
        - `clean_monogram_statistics.csv`
        - `clean_digram_statistics.csv`
        - `clean_trigram_statistics.csv`
        - `no_white_monogram_statistics.csv`
        - `no_white_digram_statistics.csv`
        - `no_white_trigram_statistics.csv`

3. **Optimization**:
   - Utilized [PyMoo][https://pymoo.org], a Python framework for multi-objective optimization.
   - Implemented a multi-objective genetic algorithm (NSGA-II) to optimize the keyboard layout.
   - The optimization process considers multiple objectives simultaneously:
     - Minimizing total keyboard weight (based on key usage frequency and distance from home row)
     - Minimizing same-finger bigrams (weighted by usage)
     - Optimizing the ratio between inward and outward rolls
   - Custom weights for different languages are used to tailor the layout to specific use cases.
   - The algorithm evolves a population of keyboard layouts over multiple generations, progressively improving the designs.
   - Non-dominated sorting is used to identify the best solutions that balance all objectives.

4. **Running the Optimization**:
   - To run the optimization process, execute the `Optimize.py` script:
     ```
     python Optimize.py
     ```
   - This script sets up the optimization problem, runs the NSGA-II algorithm, and outputs the results.
   - The optimization process may take some time, depending on the number of generations and population size.
   - Results will include a set of Pareto-optimal keyboard layouts that represent different trade-offs between the objectives.

3. **Metrics**:
   - Total keyboard weight (key usage frequency * distance from home row)
   - Total same-finger bigrams (weighted by usage)
   - Ratio between inward and outward rolls

The goal was to minimize these metrics for optimal typing efficiency.

## Results

While the project successfully implemented the optimization algorithm, it was found that existing layouts, particularly the [Polyglot layout][https://sites.google.com/alanreiser.com/handsdown/home/more-variations#h.qyya9vteoeqt], outperformed the generated layouts. As a result, the project pivoted to adapting the Polyglot layout for personal use.

## Dependencies

This project uses `uv` for dependency management. To set up the project:

1. Install `uv` if you haven't already:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a new virtual environment and install dependencies:
   ```
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

## Future Work

- Explore alternative optimization methods
- Implement and evaluate additional metrics for layout efficiency
- Investigate other existing layouts for comparison and inspiration

## Resources

- [Why do we need split keyboards][https://github.com/devpew/corne-build-guide?
tab=readme-ov-file#why-do-we-need-split-keyboards]
- [design notes][https://sites.google.com/alanreiser.com/handsdown/home/design-notes]

## Contributing

Contributions to improve the optimization algorithm, add new metrics, or enhance the analysis are welcome. Please feel free to submit issues or pull requests.

## References

This project uses WikiExtractor for processing Wikipedia dumps. If you find this tool useful in your work, please cite it as:

```bibtex
@misc{Wikiextractor2015,
  author = {Giusepppe Attardi},
  title = {WikiExtractor},
  year = {2015},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/attardi/wikiextractor}}
}
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

