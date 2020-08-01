from django import template

register = template.Library()


@register.inclusion_tag('parts/pagination.html', takes_context=True)
def pagination(context, page, begin_pages=1, end_pages=1,
               before_pages=2, after_pages=2,
               template='parts/pagination.html'):
    """
    Return a Digg-like pagination,
    by splitting long list of page into 3 blocks of pages.
    """
    get_string = ''
    for key, value in context['request'].GET.items():
        if key != 'page':
            get_string += '&%s=%s' % (key, value)

    page_range = list(page.paginator.page_range)
    begin = page_range[:begin_pages]
    end = page_range[-end_pages:]
    middle = page_range[max(page.number - before_pages - 1, 0):
                        page.number + after_pages]

    if set(begin) & set(middle):  # [1, 2, 3], [2, 3, 4], [...]
        begin = sorted(set(begin + middle))  # [1, 2, 3, 4]
        middle = []
    elif begin[-1] + 1 == middle[0]:  # [1, 2, 3], [4, 5, 6], [...]
        begin += middle  # [1, 2, 3, 4, 5, 6]
        middle = []
    elif middle[-1] + 1 == end[0]:  # [...], [15, 16, 17], [18, 19, 20]
        end = middle + end  # [15, 16, 17, 18, 19, 20]
        middle = []
    elif set(middle) & set(end):  # [...], [17, 18, 19], [18, 19, 20]
        end = sorted(set(middle + end))  # [17, 18, 19, 20]
        middle = []

    if set(begin) & set(end):  # [1, 2, 3], [...], [2, 3, 4]
        begin = sorted(set(begin + end))  # [1, 2, 3, 4]
        middle, end = [], []
    elif begin[-1] + 1 == end[0]:  # [1, 2, 3], [...], [4, 5, 6]
        begin += end  # [1, 2, 3, 4, 5, 6]
        middle, end = [], []

    return {'template': template,
            'page': page,
            'begin': begin,
            'middle': middle,
            'end': end,
            'GET_string': get_string}
