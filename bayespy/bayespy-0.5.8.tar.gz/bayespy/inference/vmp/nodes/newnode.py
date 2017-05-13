

# class Gaussian():

#     def logpdf(x_Lambda_x, x_Lambda_mu, mu_Lambda_x, mu_Lambda_mu,
#                         logdet_Lambda):
#         pass


#     def kl_divergence():
#         pass


#     def blah(x_Lambda_x, x_Lambda_mu, mu_Lambda_x):
#         pass

#     def g(mu_Lambda_mu, logdet_Lambda):
#         pass

#     def f(x):
#         pass

# def gaussian_logpdf(self, x, mu, Lambda):
#     pass

# # # Define joint pdf
# # model.logpdf(
# #     {
# #         x_obs: [[...]],
# #         mu: [...],
# #         Lambda: [[...]]
# #     }
# # )

# # How to construct the model graph immutably? Nodes only store their parents.
# # Children and other necessary stuff is computed when constructing the model.
# # For instance, the mask is propagated to parents at that point.

# mu = Gaussian([0, 0], [[1, 0], [0, 1]])
# Lambda = Wishart(2, [[1, 0], [0, 1]])
# x = Gaussian(mu, Lambda, plates=(10,))
# x_obs = x.observe(data, mask=mask)

# model = Model(x_obs, mu, Lambda)

# # How to construct arbitrary models? It is also possible to just provide an
# # arbitrary logpdf function without the Model class (or actually, by writing a
# # custom Model classes). The function logpdf takes a dictionary and
# # computes the logpdf?

# class MyArbitraryModel():
#     def logpdf(self):
#         return 0.5
# model = MyArbitraryModel()


# # How to handle cancelling out of terms in the lower bound when using
# # conjugate-exponential family nodes? In particular, the term f(x) cancels out.
# #
# # ANSWER: Consider nodes as units of random variables and use KL divergence.
# # That is, don't even try to support using some q for only part of a node. Or
# # use SymPy and hope it's able to cancel out the terms?
# #
# # Use SymPy to construct the model etc and then convert to Tensorflow (or
# # Theano)
# #
# # See: https://github.com/sympy/sympy/issues/11420


# # Should be possible to construct joint q distributions even if the variables
# # weren't in the same node in the model construction.
# #
# # ANSWER: This might require some symbolic analysis because a random variable
# # might have gone through many operations before it appears jointly with the
# # variable it has joint q with. This requires symbolic analysis and compilation
# # of the q structure. Would SymPy help?
# #
# # See: http://docs.sympy.org/0.7.0/modules/core.html#sympy.core.expr.Expr.as_coeff_add


# # How to handle variational auto-encoder? That is, instead of learning
# # variational parameters (only), one (also) learns a function to compute the
# # parameters given, for instance, data. Thus, the parameters of the variational
# # posterior approximation can be arbitrarily complex.

# # Make it possible to put several model nodes within one Q node. Thus,
# # construction of categorical graphs would be easy and would obtain exact
# # answer. Also, Gaussian graphs would be possible, inference just needs to use
# # block-sparse Cholesky. Note that phi only corresponds to those terms that
# # actually appear, thus the sparsity. This structure (e.g., Gaussian precision
# # matrix sparsity) is built when creating the VB model.

# # Find some kind of symbolic representation of the model graph? So that it is
# # possible to find all terms in which some variables appear and how they appear
# # (what moments). Start by manually setting these or not checking at all and
# # just trusting the user does the right thing. But how to support different
# # possibilities for the moments?

# logpdf = x.T * Lambda * x + mu.T * Lambda * x + and_so_on
# [
#     [Outer('x', ['Lambda']), Quadratic('x', 'Lambda'), Identity('Lambda', ['x'])],
#     [Outer('x', 'mu', ['Lambda'])]
# ]

# # How to support variational methods based on Gaussian quadrature?

# # How to support variational methods based on other variational approximations
# # as in logit regression?

# # If a model wants to support VMP, it must provide the required moments for its
# # inputs.

# vb_model = VB(
#     model,
#     {
#         (mu, Lambda): GaussianWishart
#     }
# )

# # Again, VB model can be arbitrary. It should just have a function which maps
# # from the variational parameters to the lower bound?

# # state of q are some nice parameters allowing efficient computation of
# # expectations, samples, etc
# #
# # q = compute_q(q, parameters)
# # u = compute_moments(q)

# class GaussianQ():

#     def __init__(self, GaussianNaturalParameters):
#         mu_phi1 = params['q_mu_phi1']
#         mu_phi2 = params['q_mu_phi2']
#         self.std = -2 / mu_phi2
#         self.mean = mu_u2 * mu_phi1

#     def compute_moments(self):
#         u1 = self.mean
#         u2 = self.mean ** 2 + self.std ** 2
#         return GaussianMoments(u1, u2)

#     def draw_sample(self):
#         return Sample(self.mean + self.std * np.random.randn())


# def vb_model(model, params):
#     q_mu_phi1 = params['q_mu_phi1']

#     mu


# # Mapping q <-> theta:
# #
# # Mapping p <-> q
# #
# # - compute gradient (and cost) w.r.t. theta

# # Variational parameters
# q_mu_phi1
# q_mu_phi2
# q_Lambda_phi1
# q_Lambda_phi2

# q_mu = Gaussian(shape=(2,), plates=())
# q_mu = FromPrior(mu)

# q_Lambda = Wishart(shape=(2,))

# model, vb_model, vb_parameters

# cost = vb_cost(model, vb_model)

# d = gradient(model, vb_model, [q_mu_phi1, q_mu_phi2])

# vb_parameters = vmp(model, vb_model, vb_parameters)

# # Define VB
# #q = VB(model)

# vmp()

# # Compute the lower bound
# q.lower_bound()
