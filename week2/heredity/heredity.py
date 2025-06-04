import csv
import itertools
import sys

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

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredi.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


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


# def prob_parents_mutation(person, people, one_gene, two_genes, have_trait):
#     """
#     Get the mutation prob given the info of the parents
#     """

#     # Get the mother and check copies
#     mother = people[person]["mother"]
#     mother_genes = check_how_many_copies(mother, one_gene, two_genes)

#     # Get the father and check copies
#     father = people[person]["father"]
#     father_genes = check_how_many_copies(father, one_gene, two_genes)

#     # If has 2 copies it will pass 1 for sure, if has 1 copy there is 50%
#     # chances of passing
#     prob_mother_pass_gene = mother_genes / 2
#     prob_father_pass_gene = father_genes / 2

#     p_mother_pass_gene_and_dont_mutate = prob_mother_pass_gene * (1 - PROBS["mutation"])
#     p_mother_pass_gene_and_do_mutate = prob_mother_pass_gene * PROBS["mutation"]
#     p_mother_dont_pass_gene_and_dont_mutate = (1 - prob_mother_pass_gene) * (1 - PROBS["mutation"])
#     p_mother_dont_pass_gene_and_do_mutate = (1 - prob_mother_pass_gene) * PROBS["mutation"]

#     p_father_pass_gene_and_do_mutate = prob_father_pass_gene * PROBS["mutation"]
#     p_father_pass_gene_and_dont_mutate = prob_father_pass_gene * (1 - PROBS["mutation"])
#     p_father_dont_pass_gene_and_dont_mutate = (1 - prob_father_pass_gene) * (1 - PROBS["mutation"])
#     p_father_dont_pass_gene_and_do_mutate = (1 - prob_father_pass_gene) * PROBS["mutation"]

#     child_genes = check_how_many_copies(person, one_gene, two_genes)

#     if child_genes == 0:
#         mutation_prob = (p_father_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_dont_mutate) + \
#             (p_father_pass_gene_and_do_mutate * p_mother_pass_gene_and_do_mutate) + \
#                 (p_father_dont_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_dont_mutate) + \
#                     (p_father_dont_pass_gene_and_dont_mutate * p_mother_pass_gene_and_do_mutate)
#     elif child_genes == 1:
#         mutation_prob = (p_father_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_dont_mutate) + \
#             (p_father_pass_gene_and_dont_mutate * p_mother_pass_gene_and_do_mutate) + \
#                 (p_father_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_do_mutate) + \
#                     (p_father_pass_gene_and_do_mutate * p_mother_pass_gene_and_dont_mutate) + \
#                         (p_father_dont_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_dont_mutate) + \
#                             (p_father_dont_pass_gene_and_do_mutate * p_mother_pass_gene_and_do_mutate) + \
#                                 (p_father_dont_pass_gene_and_dont_mutate * p_mother_pass_gene_and_dont_mutate) + \
#                                     (p_father_dont_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_do_mutate)
#     elif child_genes == 2:
#         mutation_prob = (p_father_pass_gene_and_dont_mutate * p_mother_pass_gene_and_dont_mutate) + \
#             (p_father_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_do_mutate) + \
#                 (p_father_dont_pass_gene_and_do_mutate * p_mother_pass_gene_and_dont_mutate) + \
#                     (p_father_dont_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_do_mutate)

#     return mutation_prob


def inherit_prob(parent_name, one_gene, two_genes):
    """
    joint_probability helper function

    Returns the probability of a parent giving a copy of the mutated gene to their child.

    Takes:
    - parent_name - the name of the parent
    - one_gene - set of people having 1 copy of the gene
    - two_genes - set of people having two copies of the gene.
    """

    if parent_name in two_genes:
        return 1 - PROBS['mutation']
    elif parent_name in one_gene:
        return 0.5
    else:
        return PROBS['mutation']


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

    # probability = 1
    # is_parent = False

    # for person, details in people.items():
    #     # If has no mother nor father, it is a parent
    #     if not details['mother'] and not details['father']:
    #         is_parent = True

    #     # Get the number of copies of the gene
    #     copies = check_how_many_copies(person, one_gene, two_genes)
    #     # has_trait = check_trait(person, have_trait)

    #     # Check if person has trait
    #     if person in have_trait:
    #         has_trait = True
    #     else:
    #         has_trait = False

    #     # Conditional probability
    #     cond_prob = PROBS["trait"][copies][has_trait]
    #     if is_parent:
    #         # Unconditional probability
    #         uncond_prob = PROBS["gene"][copies]
    #         probability *= uncond_prob * cond_prob
    #     # Children
    #     else:
    #         # mutation_prob = 0.9802
    #         mutation_prob = prob_parents_mutation(person, people, one_gene, two_genes, have_trait)
    #         probability *= mutation_prob * cond_prob

    joint_prob = 1

    # Iterate all people in the family:

    for person in people:

        person_prob = 1
        person_genes = (2 if person in two_genes else 1 if person in one_gene else 0)
        person_trait = person in have_trait

        mother = people[person]['mother']
        father = people[person]['father']

        # If person has no parents, use standard gene probability:
        if not mother and not father:
            person_prob *= PROBS['gene'][person_genes]

        # Otherwise need to calculate probabilit of num_genes from parents:
        else:
            mother_prob = inherit_prob(mother, one_gene, two_genes)
            father_prob = inherit_prob(father, one_gene, two_genes)

            if person_genes == 2:
              person_prob *= mother_prob * father_prob
            elif person_genes == 1:
              person_prob *= (1 - mother_prob) * father_prob + (1 - father_prob) * mother_prob
            else:
              person_prob *= (1 - mother_prob) * (1 - father_prob)

        # Multiply by the probability of the person with X genes having / not having the trait:
        person_prob *= PROBS['trait'][person_genes][person_trait]

        joint_prob *= person_prob

    # return probability
    # Return the calculated joint probability of this 'possible world'
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        # Get number of copies of the gene
        copies = check_how_many_copies(person, one_gene, two_genes)

        # Check if person has trait
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        # Updates
        probabilities[person]["gene"][copies] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        #
        total_gene_prob = sum(probabilities[person]["gene"].values())

        # Avoids 0 division
        if (total_gene_prob > 0):
            probabilities[person]["gene"][2] /= total_gene_prob
            probabilities[person]["gene"][1] /= total_gene_prob
            probabilities[person]["gene"][0] /= total_gene_prob

        #
        total_trait_prob = sum(probabilities[person]["trait"].values())

        # Avoids 0 division
        if (total_trait_prob > 0):
            probabilities[person]["trait"][True] /= total_trait_prob
            probabilities[person]["trait"][False] /= total_trait_prob

        # # Get probabilities of genes
        # gene2_prob = probabilities[person]["gene"][2]
        # gene1_prob = probabilities[person]["gene"][1]
        # gene0_prob = probabilities[person]["gene"][0]

        # # Get proporions of the probabilities
        # proportion1 = gene2_prob / gene1_prob
        # proportion2 = gene2_prob / gene0_prob

        # # Get new probs
        # gene2_prob = (proportion1 * proportion2) / (proportion1 * proportion2 + proportion1 + proportion2)
        # gene1_prob = gene2_prob / proportion1
        # gene0_prob = gene2_prob / proportion2

        # # Update values in probabilities
        # probabilities[person]["gene"][2] = gene2_prob
        # probabilities[person]["gene"][1] = gene1_prob
        # probabilities[person]["gene"][0] = gene1_prob

        # # Get probabilities of traits
        # trait_true = probabilities[person]["trait"][True]
        # trait_false = probabilities[person]["trait"][False]

        # # Get proportion
        # proportion_trait = trait_true / trait_false

        # # Get new probs
        # trait_true = proportion_trait / (1 + proportion_trait)
        # trait_false = 1 - trait_true

        # # Update values in probabilities
        # probabilities[person]["trait"][True] = trait_true
        # probabilities[person]["trait"][False] = trait_false


if __name__ == "__main__":
    main()
