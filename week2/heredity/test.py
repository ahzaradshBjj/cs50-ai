from itertools import islice

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

def main():
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        "person": {
            "gene": {
                2: 0.2,
                1: 0.1,
                0: 0.2
            },
            "trait": {
                True: 0.2,
                False: 0.2
            }
        }
    }

    people = {
        'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
        'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
        'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
    }
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James"}

    joint_probability(people, one_gene, two_genes, have_trait)
    normalize(probabilities)


def check_how_many_copies(person, one_gene, two_genes):
    """
    Check the number of genes that the persone has
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def prob_parents_mutation(person, people, one_gene, two_genes, have_trait):
    """
    adas
    """
    prob = 0

    return prob


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    probability = 1
    is_parent = False

    for person, details in people.items():
        # If has no mother nor father, it is a parent
        if not details['mother'] and not details['father']:
            is_parent = True

        copies = check_how_many_copies(person, one_gene, two_genes)
        # has_trait = check_trait(person, have_trait)

        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        # Conditional probability
        cond_prob = PROBS["trait"][copies][has_trait]
        if is_parent:
            # Unconditional probability
            uncond_prob = PROBS["gene"][copies]
            probability *= uncond_prob * cond_prob
        # Children
        else:
            mutation_prob = prob_parents_mutation(person, people, one_gene, two_genes, have_trait)
            #0.9802
            probability *= mutation_prob * cond_prob

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # Get probabilities of genes
    gene2_prob = probabilities["person"]["gene"][2]
    gene1_prob = probabilities["person"]["gene"][1]
    gene0_prob = probabilities["person"]["gene"][0]

    # Get proporions of the probabilities
    proportion1 = gene2_prob / gene1_prob
    proportion2 = gene2_prob / gene0_prob

    # Get new probs
    gene2_prob = (proportion1 * proportion2) / (proportion1 * proportion2 + proportion1 + proportion2)
    gene1_prob = gene2_prob / proportion1
    gene0_prob = gene2_prob / proportion2

    # Update values in probabilities
    probabilities["person"]["gene"][2] = gene2_prob
    probabilities["person"]["gene"][1] = gene1_prob
    probabilities["person"]["gene"][0] = gene1_prob

    # Get probabilities of traits
    trait_true = probabilities["person"]["trait"][True]
    trait_false = probabilities["person"]["trait"][False]

    # Get proportion
    proportion_trait = trait_true / trait_false

    # Get new probs
    trait_true = proportion_trait / (1 + proportion_trait)
    trait_false = 1 - trait_true

    # Update values in probabilities
    probabilities["person"]["trait"][True] = trait_true
    probabilities["person"]["trait"][False] = trait_false

    print("ga")
    #raise NotImplementedError

if __name__ == "__main__":
    main()
