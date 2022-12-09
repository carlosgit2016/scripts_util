'''
    Given an environment return the first failed build
'''
import argparse
import json
from pybuildkite.buildkite import Buildkite
from pybuildkite.buildkite import BuildState


def filter_by_environment(build, environment):
    if 'env' in build:
        if 'ENVIRONMENT' in build['env']:
            return build['env']['ENVIRONMENT'] == environment and build['blocked'] == False


def run(environment, org, pipeline, buildkite_token, pages=10):
    '''
        Given an environment <env> return the first failed build along side with the set of blocked / successfully that it founds
    '''
    buildkite = Buildkite()
    buildkite.set_access_token(buildkite_token)
    build = buildkite.builds()
    builds = []

    print(f'Retrieving builds from {pipeline} in branch in master')
    print(f'Limit of pages {pages}')
    response = build.list_all_for_pipeline(org, pipeline, branch="master", states=[                                                  
                                         BuildState.FAILED, BuildState.PASSED], with_pagination=True, page=0)

    while response.next_page and response.next_page < pages:
        print(f'Requesting page {response.next_page} of {pages}')
        response = build.list_all_for_pipeline(org, pipeline, branch="master", states=[
                                        BuildState.FAILED, BuildState.PASSED], with_pagination=True, page=response.next_page)
        builds.extend(response.body)

    print(f'Total of builds to filter: {len(builds)}')
    builds_from_environment = list(
        filter(lambda b: filter_by_environment(b, environment), builds))

    b_failed = None
    for b in builds_from_environment:
        print(f'Analysing {b["web_url"]} state {b["state"]}')
        if b['state'] == 'failed':
            b_failed = b
        elif b['state'] == 'passed':
            if None == b_failed:
                print('\n\n\nNo FAILED BUILD found')
                print('\n\n\nLAST PASSED BUILD {b["web_url"]} \n Bitbucket https://bitbucket.trimble.tools/projects/efs/repos/{pipeline}/commits/{b["commit"]}')
            else:
                print(f'\n\n\nLAST FAILED BUILD {b_failed["web_url"]} \nBitbucket https://bitbucket.trimble.tools/projects/efs/repos/{pipeline}/commits/{b_failed["commit"]} \n\nLAST PASSED BUILD {b["web_url"]} \n Bitbucket https://bitbucket.trimble.tools/projects/efs/repos/{pipeline}/commits/{b["commit"]}')
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Return the first failed build', prog='check_efs_environment')

    parser.add_argument('--environment', required=True,
                        metavar='environment', help='EFS environment')
    parser.add_argument('--org', required=True, metavar='org',
                        help='The name of the buildkite org')
    parser.add_argument('--pipeline', required=True, metavar='pipeline',
                        help='The name of the buildkite pipeline')
    parser.add_argument('--buildkite-token', required=True,
                        metavar='buildkite_token', help='Buildkite token')
    parser.add_argument('--total-of-pages', required=False,
                        metavar='total_of_pages', help='Total of build pages to include', default=10)

    args = parser.parse_args()
    run(args.environment, args.org, args.pipeline, args.buildkite_token, args.total_of_pages)
