'''
Created on 06 apr 2017

@author: jimmijamma
'''
from numpy import sum,log


def logz(x):
    if (x > 0):
        y = log(x)
    else:
        y = 0
    return y


def RPDE_main(mono_data, m, tau, epsilon):

    res = close_ret(mono_data, m, tau, epsilon)
    
    res = list(res)
    s = sum(res)
    rpd = []
    for element in res:
        rpd.append(1.0*element/s)
  
    N = len(rpd)
    
    H = 0
    for j in range (0,N-1):
        H = H - rpd[j] * logz(rpd[j])

    H_norm = 1.0*H/log(N)

    return H_norm, rpd


def embedSeries(embedDims,embedDelay,embedElements,inputSequence,embeddedSequence):
    # /* Create embedded version of given sequence */
    
    #  unsigned long embedDims,      /* Number of dimensions to embed */
    #  unsigned long embedDelay,     /* The embedding delay */
    #   unsigned long embedElements,  /* Number of embedded points in embedded sequence */
    #   REAL          *x,             /* Input sequence */
    #   REAL          *y              /* (populated) Embedded output sequence */

    x=inputSequence
    y=embeddedSequence
    for d in range (0,embedDims-1):
        inputDelay = (embedDims - d - 1) * embedDelay
        for i in range(0,embedElements-1):
            y[i * embedDims + d] = x[i + inputDelay]
            
    return y



def findCloseReturns(inputSequence, epsilon, embedElements, embedDims):

    # /* Search for first close returns in the embedded sequence */
    
    #   REAL           *x,               /* Embedded input sequence */
    #   REAL           eta,              /* Close return distance */
    #   unsigned long  embedElements,    /* Number of embedded points */
    #   unsigned long  embedDims,        /* Number of embedding dimensions */
    #   unsigned int   *closeRets        /* Close return time histogram */
    x=inputSequence
    eta=epsilon
    eta2 = eta * eta

    closeRets=[0]*embedElements
    
    for i in range(0,embedElements-1):
        j = i + 1
        etaFlag = False 
          
        while ((j < embedElements) and etaFlag==False): 
            dist2 = 0.0
            for d in range(0,embedDims-1):
                diff   = x[i * embedDims + d] - x[j * embedDims + d]
                dist2 = dist2 + diff * diff

            if (dist2 > eta2):
                etaFlag = True
            
            j=j+1
        
        etaFlag = False
        while ((j < embedElements) and etaFlag==False): 
            dist2 = 0.0
            for d in range(0,embedDims-1):
                diff   = x[i * embedDims + d] - x[j * embedDims + d]
                dist2 += diff * diff;

            if (dist2 <= eta2):
                timeDiff = j - i
                closeRets[timeDiff]=closeRets[timeDiff]+1
                etaFlag = True

            j=j+1





/* Main entry point */
/* lhs - output parameters */
/* rhs - input parameters */
void mexFunction(
    int           nlhs,           /* number of expected outputs */
    mxArray       *plhs[],        /* array of pointers to output arguments */
    int           nrhs,           /* number of inputs */
#if !defined(V4_COMPAT)
    const mxArray *prhs[]         /* array of pointers to input arguments */
#else
    mxArray *prhs[]         /* array of pointers to input arguments */
#endif
)
{
   long           rows, columns, vectorElements, embedElements, i;
   unsigned long  embedDims, embedDelay;
   REAL           etaIn;
   
   REAL           *CRSOut;          /* Output vector of close return counts */
   REAL           *sequenceIn;      /* Input vector */
   unsigned long  *closeRets;       /* Close return counts */
   REAL           *embedSequence;   /* Embedded input vector */

   /* Check for proper number of arguments */
   if ((nrhs != 4) || (nlhs != 1))
   {
      mexErrMsgTxt("Incorrect number of parameters.\nSyntax: "SYNTAX);
   }

   /* Checks on input sequence vector */
   rows           = mxGetM(X_IN);
   columns        = mxGetN(X_IN);
   vectorElements = columns * rows;
   if (columns != 1)
   {
      mexErrMsgTxt("Input sequence must be a row vector.");
   }
   if (!mxIsDouble(X_IN) || mxIsComplex(X_IN))
   {
      mexErrMsgTxt("Input sequence must be floating-point real.");
   }
   sequenceIn = mxGetPr(X_IN);

   /* Checks on close return distance */
   if (!mxIsDouble(ETA_IN) || mxIsComplex(ETA_IN))
   {
      mexErrMsgTxt("Close return distance eta must be floating-point real.");
   }
   etaIn = *mxGetPr(ETA_IN);

   /* Checks on embedding dimension */
   if (!mxIsNumeric(EMBEDDIM_IN) || mxIsComplex(EMBEDDIM_IN))
   {
      mexErrMsgTxt("Embedding dimension must be an integer.");
   }
   embedDims = (unsigned long)*mxGetPr(EMBEDDIM_IN);

   /* Checks on embedding delay */
   if (!mxIsNumeric(EMBEDDEL_IN) || mxIsComplex(EMBEDDEL_IN))
   {
      mexErrMsgTxt("Embedding delay must be an integer.");
   }
   embedDelay = (unsigned long)*mxGetPr(EMBEDDEL_IN);

   /* Create embedded version of input sequence */
   embedElements = vectorElements - ((embedDims - 1) * embedDelay);
   embedSequence = (REAL *)mxCalloc(embedElements * embedDims, sizeof(REAL));
   embedSeries(embedDims, embedDelay, embedElements, sequenceIn, embedSequence);

   /* Find close returns */
   closeRets = (unsigned long *)mxCalloc(embedElements, sizeof(unsigned long));
   findCloseReturns(embedSequence, etaIn, embedElements, embedDims, closeRets);

   /* Create output vectors, get pointer access */
   CRS_OUT = mxCreateDoubleMatrix(embedElements, 1, mxREAL);
   CRSOut  = mxGetPr(CRS_OUT);
   for (i = 0; i < embedElements; i ++)
   {
      CRSOut[i] = closeRets[i];
   }

   /* Release allocated memory. */
   mxFree(embedSequence);
   mxFree(closeRets);

   return;
}
