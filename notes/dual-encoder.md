### Dual Encoder Networks

* State of the art
  * Lowe et al, 2017: 0.552, 0.721, 0.9524
  * Baudis & Sedvy, 2016: 0.671, 0.805, 0.953

* Paper: `Training End-to-End Dialogue Systems with the Ubuntu Dialogue Corpus` [Link](https://www.google.co.in/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwjq6dzn_bXXAhUFS48KHZHUCzYQFggnMAA&url=http%3A%2F%2Fwww.cs.toronto.edu%2F~lcharlin%2Fpapers%2Fubuntu_dialogue_dd17.pdf&usg=AOvVaw3yTYIqpoxwiQSVpEwvHye4)

* Section 4.3

#### Experiment 1
* Units: 64
* Batch_Size: 64
* Optimizer: Adam, Learning_rate = 0.001
* Vocab-Size: 10000
* Try dropout=0.0, 0.2, 0.4., 0.6, 0.8

* Results
  * dr=0.6: Eval Loss: 0.4090, Train Loss: 0.3501, Step: 277K, 24h

#### Experiment 2
Same as Exp1, but vocab=5k

* Results:
  * Eval Loss: 0.4046 Step: 280K, Train Loss: 0.3824
  * dr=0.6 R@1:0.6026 R@2: 0.7721 R@5:0.9534

#### Experiment 3
`ctx-siamese` loss does not go below 0.51 
