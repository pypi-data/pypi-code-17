

# Prior

def logpdf(x, mu, Lambda):
    pass


def logpdf(u_x, u_mu, u_Lambda):
    pass


def logpdf(u_x, u_mu_Lambda):
    pass


def logpdf(u):
    pass


# Posterior

def logpdf(x, phi):
    pass


def logpdf(u, phi):
    pass


def moments(phi):
    pass


def random(phi):
    pass


mu = Gaussian(0, 1)
Lambda = Wishart(5, np.identity(3))

x = Gaussian(mu, Lambda)

Q = VB(
    (mu, x), # model jointly
    Lambda
)


# In general:

def logpdf(z):
    pass

def q(z):
    pass


VB(logpdf, q)
