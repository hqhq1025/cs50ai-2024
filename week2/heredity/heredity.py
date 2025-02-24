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
        sys.exit("Usage: python heredity.py data.csv")
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
    total_prob = 1
    for person in people:   #遍历所有的人
        if person in one_gene:  #根据 gene 的数量进行提取并赋值
            gene_count = 1
        elif person in two_genes:
            gene_count = 2
        else:
            gene_count = 0
        trait = person in have_trait  #提取性状
        mo = people[person]["mother"]  #提取父母，注意这里提取信息的方式
        fa = people[person]["father"]
        if not mo and not fa:  #没有父母信息，则采用随机的基因概率
            prob = PROBS["gene"][gene_count]
        else:
            mo_prob = inherit_prob(mo,one_gene, two_genes)  #这里自己写了一个辅助函数，用于计算从单亲那里遗传到基因的概率
            fa_prob = inherit_prob(fa,one_gene, two_genes)
        
            if gene_count == 2:  #两条基因，全部来自父母
                prob = mo_prob * fa_prob
            elif gene_count == 1:#一条，则需要讨论到底谁有谁没有
                prob = (1 - mo_prob) * (fa_prob) + (mo_prob) * (1 - fa_prob)
            else:  #没有，则双方都没给基因
                prob = (1 - mo_prob) * (1 - fa_prob)
        
        trait_prob = PROBS["trait"][gene_count][trait]  #从概率字典中找到性状、基因条数对应的概率（大概可以叫表现概率）
        
        final_prob = trait_prob * prob  #与遗传概率相乘，得到最终的概率
        total_prob *= final_prob  #更新总概率
        
    return total_prob
        
def inherit_prob(parent,one_gene, two_genes):
    if parent in one_gene: #如果父母只有一条，则一半的概率
        prob = 0.5
    elif parent in two_genes: #有两条，则按照概率
        prob = 1 - PROBS["mutation"]
    else: #父母没相应的基因,因而只能通过突变获得基因
        prob = PROBS["mutation"]
    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        elif person not in have_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        zero = probabilities[person]["gene"][0]
        one = probabilities[person]["gene"][1]
        two = probabilities[person]["gene"][2]
        
        ratio = 1 / (zero + one + two)
        
        probabilities[person]["gene"][0] = zero * ratio
        probabilities[person]["gene"][1] = one * ratio
        probabilities[person]["gene"][2] = two * ratio
        
        true = probabilities[person]["trait"][True]
        false = probabilities[person]["trait"][False]
        
        ratio = 1 / (true + false)
        
        probabilities[person]["trait"][True] = true * ratio
        probabilities[person]["trait"][False] = false * ratio


if __name__ == "__main__":
    main()
