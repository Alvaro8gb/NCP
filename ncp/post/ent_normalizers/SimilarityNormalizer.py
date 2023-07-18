from ncp.post.ent_normalizers.I_Normalize import I_Normalize
import ncp.post.string_similarity as ssim

class SimilarityNormalizer(I_Normalize):

    def __init__(self, values) -> None:
        self.values = values


    def normalize(self, elems:list):
        return ssim.replace_by_similar(elems, self.values)