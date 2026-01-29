# SCOPE

SCOPE: a Tree-based Self-Correcting Online Log Parsing method with Syntactic-Semantic Collaboration.
It introduces a novel bi-directional tree structure that enables efficient template matching from both forward and reverse directions, resulting in a higher overall matching rate. Additionally, it adopts a two-stage syntactic-semantic collaboration framework: a lightweight NLP model first utilizes POS information for syntax-based matching, while the LLM is selectively invoked as a fallback to handle semantically complex cases when uncertainty remains. This design significantly reduces LLM API usage while maintaining high accuracy, achieving a balance between efficiency and effectiveness.

SW framework is extented based on Drain3.


## Directory Structure

- `code/`: Core modules for masking, profiling, and template mining
- `evaluator/`: Evaluation scripts, configuration, and datasets
- `examples/`: Example scripts and configuration files

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/LogXpert/SCOPE.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run example scripts:
   ```bash
   python examples/test.py

4. Run dataset evaluation:

   ```bash
   # logHub-2K Raw Datasets
   python evaluator/evaluator.py --dataset=2k --type=raw

   # logHub-2K Corrected Datasets
   python evaluator/evaluator.py --dataset=2k --type=corrected

   # logHub-2.0 Datasets
   python evaluator/evaluator.py --dataset=full
   ```


## Result

Result can be found in result.log under running directory

**logHub-2K:**
| Dataset      | GA      | PA      | FGA     | FTA     | #Template | #LLM Call | #LLM Tokens |
|-------------|---------|---------|---------|---------|-----------|-----------|-------------|
| Proxifier   | 1        | 1        | 1        | 1        | 8         | 1         | 2414        |
| Apache      | 1        | 1        | 1        | 1        | 6         | 0         | 0           |
| OpenSSH     | 0.9985   | 0.995    | 0.9434   | 0.7547   | 27        | 8         | 20276       |
| HDFS        | 1        | 1        | 1        | 1        | 14        | 0         | 0           |
| OpenStack   | 1        | 0.939    | 1        | 0.7907   | 43        | 2         | 4625        |
| HPC         | 0.99     | 0.991    | 0.8817   | 0.7742   | 49        | 8         | 18958       |
| Zookeeper   | 0.9945   | 0.974    | 0.9159   | 0.8598   | 57        | 7         | 15548       |
| HealthApp   | 1        | 0.8645   | 1        | 0.76     | 75        | 2         | 4444        |
| Hadoop      | 0.9935   | 0.8955   | 0.9869   | 0.7598   | 115       | 6         | 13842       |
| Spark       | 0.997    | 0.994    | 0.8823   | 0.7647   | 32        | 4         | 9743        |
| BGL         | 0.9935   | 0.9475   | 0.9748   | 0.6807   | 118       | 19        | 42752       |
| Linux       | 0.997    | 0.98     | 0.961    | 0.7446   | 116       | 20        | 43940       |
| Mac         | 0.9635   | 0.6585   | 0.9448   | 0.5552   | 346       | 28        | 70500       |
| Thunderbird | 0.9585   | 0.7785   | 0.8091   | 0.5527   | 202       | 32        | 69521       |
| Windows     | 0.996    | 0.978    | 0.9159   | 0.6355   | 57        | 10        | 28515       |
| Andriod     | 0.9595   | 0.683    | 0.9379   | 0.6584   | 164       | 15        | 40197       |
| **Average** | 0.9901   | 0.9174   | 0.9471   | 0.7682   | 89.3125   | 10.125    | 24079.7     |


**logHub-2.0:**
| Dataset      | GA      | PA      | FGA     | FTA     | #Template | #LLM Call | #LLM Tokens |
|-------------|---------|---------|---------|---------|-----------|-----------|-------------|
| Proxifier   | 1       | 1       | 1       | 1       | 11        | 1         | 2387        |
| Apache      | 0.9931  | 0.9908  | 0.8437  | 0.7187  | 35        | 1         | 2190        |
| OpenSSH     | 0.9538  | 0.8391  | 0.9     | 0.825   | 42        | 10        | 23523       |
| HDFS        | 0.9941  | 0.9617  | 0.9677  | 0.8603  | 47        | 2         | 4656        |
| OpenStack   | 1       | 0.8928  | 1       | 0.8333  | 48        | 3         | 7238        |
| HPC         | 0.972   | 0.99    | 0.8511  | 0.7447  | 85        | 18        | 41040       |
| Zookeeper   | 0.9913  | 0.7983  | 0.918   | 0.7869  | 97        | 10        | 21223       |
| HealthApp   | 0.9365  | 0.5863  | 0.9283  | 0.5981  | 165       | 6         | 12955       |
| Hadoop      | 0.9875  | 0.894   | 0.9483  | 0.7327  | 250       | 14        | 33260       |
| Spark       | 1       | 0.9965  | 1       | 0.8611  | 236       | 19        | 44737       |
| BGL         | 0.8228  | 0.4467  | 0.7633  | 0.416   | 377       | 100       | 230440      |
| Linux       | 0.998   | 0.98    | 0.9741  | 0.7413  | 319       | 55        | 120859      |
| Mac         | 0.8956  | 0.4754  | 0.864   | 0.4351  | 698       | 41        | 96719       |
| Thunderbird | 0.9083  | 0.5618  | 0.8774  | 0.5319  | 1312      | 161       | 384543      |
| **Average** | 0.9609  | 0.8152  | 0.9169  | 0.7204  | 265.9     | 31.5      | 73269.3     |

## Usage

- Configure log parsing and template mining using `.ini` files in `evaluator/`.
- Use provided datasets for benchmarking and evaluation.


## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and new features.

## License

This project is open-source. See the LICENSE file for details.

