def calculate_bayes_theorem(p_a: float, p_b_given_a: float, p_b_given_not_a: float) -> float:
    """
    Calculates the posterior probability P(A|B) using Bayes' Theorem.
    
    Args:
        p_a: Prior probability of event A occurring. P(A)
        p_b_given_a: Likelihood of B occurring given A is true. P(B|A)
        p_b_given_not_a: Likelihood of B occurring given A is false. P(B|~A)
        
    Returns:
        float: The posterior probability P(A|B)
    """
    p_not_a = 1.0 - p_a
    print(f"Calculating P(A|B) with:")
    print(f"  P(A) = {p_a}")
    print(f"  P(B|A) = {p_b_given_a}")
    print(f"  P(B|~A) = {p_b_given_not_a}")
    p_b = (p_b_given_a * p_a) + (p_b_given_not_a * p_not_a)
    print(f"  P(B) = {p_b:.2f} (Total Probability of B)")
    p_a_given_b = (p_b_given_a * p_a) / p_b
    
    return p_a_given_b

if __name__ == "__main__":
    print("--- Bayesian Spam Filter Simulation ---")

    P_SPAM = 0.20
    P_WINNER_GIVEN_SPAM = 0.80
    P_WINNER_GIVEN_LEGIT = 0.05

    print(f"Prior Probability of Spam     : {P_SPAM * 100:.1f}%")
    print(f"Likelihood 'Winner' in Spam   : {P_WINNER_GIVEN_SPAM * 100:.1f}%")
    print(f"Likelihood 'Winner' in Legit  : {P_WINNER_GIVEN_LEGIT * 100:.1f}%")

    probability_spam = calculate_bayes_theorem(
        p_a=P_SPAM, 
        p_b_given_a=P_WINNER_GIVEN_SPAM, 
        p_b_given_not_a=P_WINNER_GIVEN_LEGIT
    )

    print("-" * 40)
    print(f"Posterior Probability P(Spam | 'Winner') : {probability_spam * 100:.2f}%")
    
    if probability_spam > 0.50:
        print("Classification : FLAG AS SPAM")
    else:
        print("Classification : ALLOW TO INBOX")