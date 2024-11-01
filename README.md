# workshop-data-driven-defense

<img src="res/dia_de_los_hackers.jpg" alt="dia_de_los_hackers" width="410px">

---

## Overview

This repository contains the code and resources for the **Data-Driven Defense workshop** for the 2024 *"Dia De Los Hackers"* **[Pacific Hackers Conference](https://www.phack.org/)**. The workshop focuses on the applications of machine learning to analyze network traffic logs for intrusion detection. The workshop is designed to introduce essential concepts in machine learning including data analysis, preprocessing, and model training & evaluation, with a specific focus on network traffic.

## Learning Objectives

By the end of this workshop, you will be able to:

- Familiarize with technical concepts of applied machine learning.
- Analyze and preprocess network traffic data for intrusion detection.
- Implement a machine learning model for classifying network traffic logs.
- Evaluate the performance of the model and interpret the results.

## Materials

- [Presentation slides](res/presentation.pdf)
- [Annotated paper](res/annotated_paper.pdf)

## Setup

Requires [uv](https://docs.astral.sh/uv/) and a Kaggle account.

1. Install dependencies (creates a pinned `.venv` with JupyterLab):

   ```bash
   uv sync
   ```

2. Authenticate with Kaggle. Generate a token at [kaggle.com/settings](https://www.kaggle.com/settings) and either export it or save it to a file:

   ```bash
   export KAGGLE_API_TOKEN=<your-token>
   # or: echo <your-token> > ~/.kaggle/access_token
   ```

   Then open the [Edge-IIoTset dataset page](https://www.kaggle.com/datasets/mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot) and accept its terms.

3. Download the data and build the SQLite database under `db/`:

   ```bash
   uv run python deploy.py
   ```

4. Launch the notebooks:

   ```bash
   uv run jupyter lab
   ```

## Notebooks

You can find the workshop notebooks in the `notebooks` directory. You can run these notebooks locally on your machine and use them to follow along with the workshop content. Feel free to fork this repo to experiment with the code and try out different approaches and techniques.

## Acknowledgements

Special thanks to the creators of the Edge-IIoTset dataset for making their data available for research and educational purposes. I strongly recommend checking out the research paper published by Ferrag et al. for a detailed overview of the dataset and its potential applications: [Edge-IIoTset: A New Comprehensive Realistic Cyber Security Dataset of IoT and IIoT Applications for Centralized and Federated Learning](https://arxiv.org/abs/2103.00688).

```bibtex
@ARTICLE{9751703,
  author={Ferrag, Mohamed Amine and Friha, Othmane and Hamouda, Djallel and Maglaras, Leandros and Janicke, Helge},
  journal={IEEE Access}, 
  title={Edge-IIoTset: A New Comprehensive Realistic Cyber Security Dataset of IoT and IIoT Applications for Centralized and Federated Learning}, 
  year={2022},
  volume={10},
  number={},
  pages={40281-40306},
  keywords={Industrial Internet of Things;Sensors;Temperature sensors;Computer crime;Security;Protocols;Computer security;Cybersecurity applications;IoT datasets;deep learning;federated learning;edge {computing}},
  doi={10.1109/ACCESS.2022.3165809}}
```

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). See the [LICENSE](LICENSE.md) file for the full terms and commercial-licensing contact.
