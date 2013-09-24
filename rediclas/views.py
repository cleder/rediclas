from pyramid.view import view_config
import rediclas.utils as utils
import redisbayes
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'rediclas'}


@view_config(route_name='stopwords', renderer='templates/stopwords.pt')
def stopword_view(request):
    stopwords = ''
    if request.params.get('update') and request.params.get('text'):
        utils.redis_server.delete('stopwords')
        tokens = utils.simple_preprocess(request.params['text'],
            deacc=utils.DEACCENT)
        for token in tokens:
           utils.redis_server.sadd('stopwords', token)
    stopwords = utils.redis_server.smembers('stopwords')
    if stopwords:
        stopwords = ' '.join(stopwords)
    else:
        stopwords = ''
    return {'stopwords': stopwords}

def tokenizer(text):
    tokens = utils.simple_preprocess(text,
            deacc=utils.DEACCENT)
    stopwords = utils.redis_server.smembers('stopwords')
    return (token for token in tokens if not token in stopwords)


@view_config(route_name='train', renderer='templates/training.pt')
def training_view(request):
    id = request.params.get('id', '')
    if request.params.get('update'):
        text = request.params.get('text')
        tags = [tag for tag in request.POST.getall('tag') if tag]
        if tags and id and text:
            old_tags = utils.redis_server.smembers('document:'+id)
            rb = redisbayes.RedisBayes(utils.redis_server, tokenizer=tokenizer)
            for tag in tags:
                if tag in old_tags:
                    continue
                else:
                    utils.redis_server.sadd('document:'+id, tag)
                    #train
                    rb.train(tag, text)
            for old_tag in old_tags:
                if old_tag in tags:
                    continue
                else:
                    utils.redis_server.srem('document:'+id, old_tag)
                    #untrain
                    rb.untrain(tag, text)
    new_tags = utils.redis_server.smembers('document:'+id)
    return {'tags': new_tags, 'id': id}

@view_config(route_name='classify', renderer='templates/classification.pt')
def classification_view(request):
    scores = {}
    if request.params.get('text'):
        rb = redisbayes.RedisBayes(utils.redis_server, tokenizer=tokenizer)
        scores = rb.score(request.params.get('text'))
    return {'scores': scores.items()}


